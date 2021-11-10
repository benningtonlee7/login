import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Local
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                           'mysql+pymysql://{username}:' '{password}@{host}/{db_name}'.format(username="root",
    #                                                                                              password="dbuser666",
    #                                                                                              host="localhost",
    #                                                                                              db_name="login")
    # DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+mysqlconnector://{username}:' '{password}@{host}/{db_name}'.format(username="admin",
                                                                                                 password="Columbia2021",
                                                                                                 host="ec2-db.cz3ufbylkv7z.us-east-2.rds.amazonaws.com",
                                                                                                 db_name="login")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID") or "1029189840786-4j07jl0eal7jusjrp4oaoic49ok9ujil.apps.googleusercontent.com"

    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET") or "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"

    OAUTHLIB_INSECURE_TRANSPORT = 1

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
