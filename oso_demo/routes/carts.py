from flask import Blueprint, current_app, jsonify, session
from sqlalchemy.orm import Session
from oso_demo.api.decorators import valid_user_required
from oso_demo.models import Cart, User
from typing import List, Type

carts_bp = Blueprint('carts', __name__)


@carts_bp.route('/', methods=['GET'])
def carts_by_user():
    ret_data = {}
    with Session(current_app.engine) as s:
        carts = s.query(Cart).where(User.id == uid).all()
        ret_data["carts"] = [cart.to_dict() for cart in carts]
    return jsonify(ret_data), 200

@carts_bp.route('/<string:cart_uuid>', methods=['GET'])
def cart_by_id(cart_uuid):
    return jsonify({'cart': cart_uuid}), 200

@carts_bp.route('/<string:cart_uuid>', methods=['DELETE'])
@valid_user_required
def delete_cart(cart_uuid):
    return jsonify({'deleted': cart_uuid}), 200