from flask_sqlalchemy import SQLAlchemy
from flask import session
from oso_demo.models import User
from typing import cast


# centralize access to SQLAlchemy (basic configuration)
db = SQLAlchemy()