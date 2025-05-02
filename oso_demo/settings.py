from os import environ

OSO_AUTH = environ.get("OSO_AUTH")
OSO_URL = environ.get("OSO_URL")
OSO_DATA_BINDINGS = environ.get("OSO_DATA_BINDINGS")

SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
