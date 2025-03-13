from flask import Flask
from flask_migrate import Migrate
from api.core import db
from models import *

migrate = Migrate()

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        return app.config.get("OSO_CLOUD_API_KEY")

    return app
