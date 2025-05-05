from flask import Blueprint, current_app, jsonify, request, Session
from oso_demo.models import Shop, Product
from oso_cloud import Value

shops_bp = Blueprint("shops", __name__)

@shops_bp.route("/", methods=["GET"])
def active_shops():
    """
    exercise 1: list all active shops
    """
    ret_data = {}
    uid = request.headers.get("uid")

    # TODO: oso list call here
    with Session(current_app.engine) as s:
        # TODO: add Oso list as filter below
        shops = s.query(Shop).filter().all()
        ret_data["shops"] = [shop.to_dict() for shop in shops]
    return jsonify(ret_data), 200

@shops_bp.route("/", methods=["POST"])
def create_shop():
    """
    exercise 2: create a shop
    """
    uid = request.headers.get("uid")
    data = request.json
    name = data.get("name")
    desc = data.get("desc")
    is_active = bool(data.get("is_active"))
    if name is None or type(name) is not str:
        return jsonify({"error": "name is required"}), 400
    if desc is None or type(desc) is not str:
        desc = ""
    if is_active is None or type(is_active) is not bool:
        is_active = False

    with Session(current_app.engine) as s:
        shop = Shop(name=name, description=desc, is_active=is_active, owner_id=uid)
        s.add(shop)
        s.commit()
        # todo: write one oso fact for shop ownership relationship and one for active if active
        return jsonify({"shop": shop.to_dict()}), 200

@shops_bp.route("/all_products", methods=["GET"])
def get_all_products():
    """
    exercise 3: get all active products across all active shops
    """
    uid = request.headers.get("uid")

    # todo: use list or  query interface
    with Session(current_app.engine) as s:
        # todo: add filter here
        #       can also do sorts, pagination, etc.
        products = s.query(Product).filter().all()
        return jsonify({"products": [product.to_dict() for product in products]}), 200
