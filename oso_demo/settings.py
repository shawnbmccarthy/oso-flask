from os import environ

OSO_CLOUD_API_KEY = environ.get("OSO_CLOUD_API_KEY")
OSO_URL = environ.get("OSO_URL")
DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASS")
DB_HOST = environ.get("DB_HOST")
DB_PORT = environ.get("DB_PORT")
DB_SSL = environ.get("DB_SSL")
DB = environ.get("DB")
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
