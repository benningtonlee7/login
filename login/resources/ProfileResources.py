from sqlalchemy import or_
from login import app, login, db, ma
from flask_login import UserMixin, current_user
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy.orm.exc import NoResultFound


class Address(db.Model):
    __table_name__ = "Address"
    address_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), index=True, unique=False)
    city = db.Column(db.String(120), index=True, unique=False)
    state = db.Column(db.String(10), index=True, unique=False)
    country = db.Column(db.String(30), index=True, unique=False)
    zipcode = db.Column(db.String(10), index=True, unique=False)

    # user_ids = db.relationship("Profile", back_populates="address")

    def __repr__(self):
        return '<Address: {} id:{}>'.format(self.address + ", " + self.city + ", " + self.state + ", " + self.zipcode,
                                            self.address_id)
    @classmethod
    def parse_info(cls, info):
        address_info = {"address": info["address"],
                     "city": info["city"],
                     "state": info["state"],
                     "country": info["country"],
                     "zipcode": info["zipcode"]}
        return address_info


    @classmethod
    def update(cls, address_id, info):
        new_info = cls.parse_info(info)
        address_row = Address.query.filter_by(address_id=address_id).first()
        address_row.address = new_info["address"]
        address_row.city = new_info["city"]
        address_row.country = new_info["country"]
        address_row.zipcode = new_info["zipcode"]
        return address_row



class AddressSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Address

    address_id = ma.auto_field()
    address = ma.auto_field()
    city = ma.auto_field()
    state = ma.auto_field()
    country = ma.auto_field()
    zipcode = ma.auto_field()
    # user_ids = ma.auto_field()


class Profile(UserMixin, db.Model):
    __tablename__ = 'Profile'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    userID = db.Column(db.String(64), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    last_name = db.Column(db.String(64), index=True, unique=False, nullable=False)
    address_id = db.Column(db.Integer, index=True, unique=False, nullable=False)
    address = db.Column(db.String(128), index=True, unique=False, nullable=False)

    # address_id = db.Column(db.Integer, foreign_keys=db.ForeignKey("Address.address_id"))
    # address = db.relationship('Address', backref='user_ids')

    def __repr__(self):
        return '<Profile user: {}, id: {}>'.format(self.email, self.id)

    @staticmethod
    def validate_existence(info):
        """TO-DO: might need to check if the info being passed in empty"""
        userID, email = info["userID"], info["email"]
        user = Profile.query.filter(or_(Profile.username == userID, Profile.email == email)).first()
        if user is None:
            return True
        return False

    @classmethod
    def parse_info(cls, info):
        userID, _ = info["email"].split("@")
        user_info = {"email": info["email"],
                     "userID": userID,
                     "first_name": info["given_name"],
                     "last_name": info["family_name"],
                     "address_id": info["address_id"],
                     "address": info["address"]}
        return user_info

    @classmethod
    def update(cls, id, info):
        user_row = Profile.query.filter_by(id=id).first()
        user_row.address = info["address"]
        user_row.first_name = info["first_name"]
        user_row.last_name = info["last_name"]
        return user_row

class OAuth(OAuthConsumerMixin, db.Model):
    provider = db.Column(db.String(256), unique=False, nullable=False)
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Profile.id), nullable=False)
    user = db.relationship(Profile)

    @classmethod
    def parse_info(cls, info):
        oauth_info = {"provider": info["provider"],
                      "provider_user_id": info["provider_user_id"],
                      "token": info["token"]}

        return oauth_info

    @classmethod
    def validate_existence(cls, info):
        """TO-DO: might need to check if the info being passed in empty"""

        query = OAuth.query.filter_by(provider=info["provider"], provider_user_id=info["provider_user_id"])
        try:
            oauth = query.one()
        except NoResultFound:
            oauth = OAuth(provider=info["provider"], provider_user_id=info["provider_user_id"], token=info["token"])
        return oauth


class ProfileSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Profile

    id = ma.auto_field()
    email = ma.auto_field()
    userID = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    address = ma.auto_field()


@login.user_loader
def load_profile(id):
    return Profile.query.get(int(id))

