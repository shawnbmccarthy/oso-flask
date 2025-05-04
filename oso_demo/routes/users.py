from flask import Blueprint, current_app, jsonify, request
from oso_demo.models import User
from typing import List, Type
from sqlalchemy.orm import Session

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_all_users():
    """
    list of users that can be logged in as
    """
    ret_data = {}
    with Session(current_app.engine) as session:
        users: List[Type[User]] = session.query(User).all()
        ret_data["users"] = [{"id": u.id, "name": u.name, "email": u.email} for u in users]
    return jsonify(ret_data), 200

@users_bp.route('/<string:user_id>', methods=['GET'])
def get_user(user_id: str):
    """
    list of users that can be logged in as
    """
    ret_data = {}
    uid = request.args.get('uid')
    with Session(current_app.engine) as session:
        ret_data["user" ] = session.query(User).filter(User.id == user_id).first().to_dict()
    return jsonify(ret_data), 200
