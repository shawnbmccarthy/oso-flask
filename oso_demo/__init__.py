from typing import cast

from flask import Flask
from flask_migrate import Migrate
from oso_cloud import Oso
from sqlalchemy import Engine, create_engine

from oso_demo.api.core import db
from oso_demo.api.errors import register_error_handlers
from oso_demo.routes.carts import carts_bp
from oso_demo.routes.shops import shops_bp
from oso_demo.routes.users import users_bp

migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_pyfile("settings.py")

    # add engine
    app.engine = cast(
        Engine, create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)
    )

    # add oso
    app.oso = cast(
        Oso,
        Oso(
            url=app.config["OSO_URL"],
            api_key=app.config["OSO_AUTH"],
            data_bindings=app.config["OSO_DATA_BINDINGS"],
        ),
    )

    # register routes
    app.register_blueprint(carts_bp, url_prefix="/api/v1/carts")
    app.register_blueprint(shops_bp, url_prefix="/api/v1/shops")
    app.register_blueprint(users_bp, url_prefix="/api/v1/users")

    # error handlers
    register_error_handlers(app)

    # initialize db
    db.init_app(app)
    migrate.init_app(app, db)

    return app
