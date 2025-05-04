from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.orm import Session
from oso_demo.models import Cart, CartItem, User
from oso_cloud import Value

carts_bp = Blueprint('carts', __name__)


@carts_bp.route('/', methods=['GET'])
def carts_by_user():
    """
    get cart by user, list of all carts uid can read

    We should return all carts the user owns as well as all carts that are public
    """
    ret_data = {}
    uid = request.args.get('uid')
    filter = current_app.oso.list(Value("User", uid), "view", "Cart")

    with Session(current_app.engine) as s:
        carts = s.query(Cart).filter((Cart.id.in_(filter))).all()
        ret_data["carts"] = [cart.to_dict() for cart in carts]
    return jsonify(ret_data), 200

@carts_bp.route('/<string:cart_uuid>', methods=['GET'])
def cart_by_id(cart_uuid):
    ret_data = {}
    uid = request.args.get('uid')
    with Session(current_app.engine) as s:
        cart = s.query(Cart).filter(Cart.id == cart_uuid and Cart.user_id == uid).first()
        ret_data["cart"] = cart.to_dict()
    return jsonify(ret_data), 200

@carts_bp.route('/<string:cart_uuid>', methods=['DELETE'])
def delete_cart(cart_uuid):
    uid = request.args.get('uid')
    with Session(current_app.engine) as s:
        s.query(Cart).filter((Cart.id == cart_uuid) & (Cart.user_id == uid)).delete()
    return jsonify({'deleted': cart_uuid}), 200

@carts_bp.route("/<string:cart_uuid>/items", methods=["GET"])
def cart_items(cart_uuid):
    uuid = request.args.get("uuid")
    ret_data = {}
    with Session(current_app.engine) as s:
        cart_items = s.query(CartItem).filter(CartItem.cart_id == cart_uuid)
        ret_data = {"cart_items": [cart_item.to_dict() for cart_item in cart_items]}

    return jsonify(ret_data), 200

@carts_bp.route("/<string:cart_uuid>/items", methods=["POST"])
def add_cart_item(cart_uuid):
    uuid = request.args.get("uuid")
    pid = request.args.get("pid")
    quantity = int(request.args.get("quantity"))

    ret_data = {}
    with Session(current_app.engine) as s:
        cart_item = CartItem(cart_id=cart_uuid, product_id=pid, quantity=quantity)
        s.add(cart_item)
        s.commit()
        ret_data["cart_item"] = cart_item.to_dict()
    return jsonify(ret_data), 200

@carts_bp.route("/<string:cart_uuid>/items/<string:ci_uuid>", methods=["DELETE"])
def delete_cart_item(cart_uuid, ci_uuid):
    uuid = request.args.get("uuid")
    i = 0
    with Session(current_app.engine) as s:
        i = s.query(CartItem).filter((CartItem.cart_id == cart_uuid) & (CartItem.id == ci_uuid)).delete()
        s.commit()
    return jsonify({"deleted": ci_uuid, "i": i}), 200
