from os import environ

OSO_CLOUD_API_KEY = environ.get("OSO_CLOUD_API_KEY")
OSO_URL = environ.get("OSO_URL")

SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
