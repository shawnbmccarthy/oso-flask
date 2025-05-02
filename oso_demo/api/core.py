from flask_sqlalchemy import SQLAlchemy
from flask import session
from oso_demo.models import User
from typing import cast


# centralize access to SQLAlchemy (basic configuration)
db = SQLAlchemy()

# helpers
def get_current_user() -> User | None:
    if not session.get("current_user"):
        return None
    return cast(User, session["current_user"])

def set_current_user(user: User) -> None:
    if not session.get("current_user"):
        session["current_user"] = user

