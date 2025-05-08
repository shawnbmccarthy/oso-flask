import json

from flask import Blueprint, current_app, jsonify, request
from sqlalchemy.orm import Session
from oso_demo.models import Cart, CartItem, User
from oso_cloud import Value

carts_bp = Blueprint("carts", __name__)


@carts_bp.route("/", methods=["GET"])
def carts_by_user():
    """
    exercise 1: get cart by user, list of all carts uid can read

    We should return all carts the user owns as well as all carts that are public
    """
    ret_data = {}
    uid = request.headers.get("uid")

    # TODO: oso list call here

    with Session(current_app.engine) as s:
        # TODO: add Oso list as filter below
        carts = s.query(Cart).filter().all()
        ret_data["carts"] = [cart.to_dict() for cart in carts]
    return jsonify(ret_data), 200

@carts_bp.route("/", methods=["POST"])
def create_cart():
    """
    exercise 2: create a cart for a user
    """
    uid = request.headers.get("uid")
    data = request.json
    is_public = bool(data.get("is_public"))
    if is_public is None or type(is_public) is not bool:
        is_public = False

    with Session(current_app.engine) as s:
        cart = Cart(user_id=uid, is_public=is_public)
        s.add(cart)
        s.commit()
        # todo: write one oso fact for cart ownership relationship
        #       if cart is public, then one fact for public
        return jsonify({"cart": cart.to_dict()}), 200

@carts_bp.route("/<string:cart_uuid>", methods=["GET"])
def cart_by_id(cart_uuid):
    """
    Exercise 3: attempt to get read a cart

    Result: only public carts or carts owned by user can be read
    """
    ret_data = {}
    uid = request.headers.get("uid")
    # TODO: authorize if the user is allowed to read the cart
    #       can we make this a decorator?
    with Session(current_app.engine) as s:
        # TODO: oso filter here
        cart = s.query(Cart).filter().first()
        ret_data["cart"] = cart.to_dict()
    return jsonify(ret_data), 200

@carts_bp.route("/<string:cart_uuid>", methods=["DELETE"])
def delete_cart(cart_uuid):
    """
    Exercise 4: user should only be allowed to delete their own carts
    """
    uid = request.headers.get("uid")

    # TODO: is user allowed to delete cart?

    with Session(current_app.engine) as s:
        s.query(Cart).filter(Cart.id == cart_uuid).delete()
        s.commit()
        # TODO: delete has_relation fact
        #       if public, is_public fact
    return jsonify({"deleted": cart_uuid}), 200

@carts_bp.route("/<string:cart_uuid>/items", methods=["GET"])
def cart_items(cart_uuid):
    """
    exercise 5: get all items in a cart
    """
    uuid = request.headers.get("uuid")

    # TODO: is user allowed to read cart?
    ret_data = {}
    with Session(current_app.engine) as s:
        cart_items = s.query(CartItem).filter(CartItem.cart_id == cart_uuid).all()
        ret_data = {"cart_items": [cart_item.to_dict() for cart_item in cart_items]}

    return jsonify(ret_data), 200

@carts_bp.route("/<string:cart_uuid>/items", methods=["POST"])
def add_cart_item(cart_uuid):
    """
    exercise 6: add new item to a cart, a user should only be allowed to add items to
    their own carts
    """
    uuid = request.headers.get("uuid")

    # TODO: is user allowed to update cart?

    data = request.json
    pid = data.get("pid")
    quantity = int(data.get("quantity"))

    ret_data = {}
    with Session(current_app.engine) as s:
        """
        Note: product business logic left out for simplicity
        """
        cart_item = CartItem(cart_id=cart_uuid, product_id=pid, quantity=quantity)
        s.add(cart_item)
        s.commit()
        ret_data["cart_item"] = cart_item.to_dict()
    return jsonify(ret_data), 200

@carts_bp.route("/<string:cart_uuid>/items/<string:ci_uuid>", methods=["DELETE"])
def delete_cart_item(cart_uuid, ci_uuid):
    """
    exercise 7: a user should only be able to remove items from their own carts
    """
    uuid = request.headers.get("uuid")

    # todo: is user allowed to update cart?

    i = 0
    with Session(current_app.engine) as s:
        i = s.query(CartItem).filter((CartItem.cart_id == cart_uuid) & (CartItem.id == ci_uuid)).delete()
        s.commit()
    return jsonify({"deleted": ci_uuid, "i": i}), 200
