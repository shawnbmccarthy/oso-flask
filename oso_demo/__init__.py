from flask import Flask
from flask_migrate import Migrate
from flask_session import Session
from cachelib import SimpleCache
from typing import cast
from oso_cloud import Oso
from sqlalchemy import create_engine, Engine
from oso_demo.api.core import db
from oso_demo.api.errors import register_error_handlers
from oso_demo.routes.carts import carts_bp
from oso_demo.routes.shops import shops_bp
from oso_demo.routes.users import users_bp
from oso_demo.views.home_views import app_views_bp

migrate = Migrate()

def create_app() -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_pyfile("settings.py")

    # setup session
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_COOKIE_SECURE"] = False
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SECRET_KEY"] = "dev"
    app.config["SESSION_CACHELIB"] = SimpleCache()
    app.config["SESSION_TYPE"] = "cachelib"

    # add engine
    app.engine = cast(Engine, create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True))

    # add oso
    app.oso = cast(Oso, Oso(
        url=app.config["OSO_URL"],
        api_key=app.config["OSO_AUTH"],
        data_bindings=app.config["OSO_DATA_BINDINGS"]
    ))

    Session(app)

    # register routes
    app.register_blueprint(carts_bp, url_prefix="/api/v1/carts")
    app.register_blueprint(shops_bp, url_prefix="/api/v1/shops")
    app.register_blueprint(users_bp, url_prefix="/api/v1/users")

    # register views
    app.register_blueprint(app_views_bp, template_folder="templates")

    # error handlers
    register_error_handlers(app)

    # initialize db
    db.init_app(app)
    migrate.init_app(app, db)

    return app
