from login import db
from login.config import Config
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.consumer import oauth_authorized, oauth_error
from login.resources.ProfileResources import OAuth, Profile
from sqlalchemy.orm.exc import NoResultFound
from flask_login import current_user, login_user
from flask import flash, redirect, url_for

google_blueprint = make_google_blueprint(
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    scope=['https://www.googleapis.com/auth/userinfo.email',
           'https://www.googleapis.com/auth/userinfo.profile'],
    offline=True,
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    )
)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.", category="error")
        return False

    resp = blueprint.session.get("/oauth2/v1/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False
    info = resp.json()
    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(provider=blueprint.name, provider_user_id=info["id"])
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name, provider_user_id=info["id"], token=token)

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with Google.")

    else:
        # Create a new local user account for this user
        info["address_id"] = 1
        info["address"] = "abc"
        userID, _ = info["email"].split("@")
        user_info = {"email": info["email"],
                     "userID": userID,
                     "first_name": info["given_name"],
                     "last_name": info["family_name"],
                     "address_id": info["address_id"],
                     "address": info["address"]}

        user = Profile(**user_info)
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with Google.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False

@oauth_authorized.connect
def logged_in(blueprint, token):
    flash("Signed in successfully with {name}!".format(name=blueprint.name.capitalize()))
    return redirect(url_for("profile"))

# notify on OAuth provider error
@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, message, response):
    msg = "OAuth error from {name}! " "message={message} response={response}".format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")
