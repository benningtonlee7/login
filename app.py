from login import app, db
from login.resources.ProfileResources import Profile, Address


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Profile': Profile, 'Address': Address}