from functools import wraps
from flask import session
from .errors import InvalidApiUsage

def valid_user_required(f):
    """
    simple decorator to check session contains a valid user
    Note: this is not production ready, just for demo purposes
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("uid"):
            raise InvalidApiUsage(f"User not logged in", status_code=401)
        return f(*args, **kwargs)
    return decorated