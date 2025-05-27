from flask import Blueprint, current_app, jsonify, request

# from oso_cloud import Value
from sqlalchemy.orm import Session

from oso_demo.models import Product, Shop

shops_bp = Blueprint("shops", __name__)


@shops_bp.route("/", methods=["GET"])
def active_shops():
    """
    exercise 1: list all active shops
    """
    ret_data = {}
    uid = request.headers.get("uid")

    # TODO: what shops can the user see? (list)

    with Session(current_app.engine) as s:
        # TODO: add Oso list as filter below
        shops = s.query(Shop).filter().all()
        ret_data["shops"] = [shop.to_dict() for shop in shops]
    return jsonify(ret_data), 200


@shops_bp.route("/", methods=["POST"])
def create_shop():
    """
    exercise 2: create a shop, every user can create a shop
                creating a shop requires oso data for authorized access to
                the shop
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
        # TODO: write one oso fact for shop ownership relationship and one for active if active
        return jsonify({"shop": shop.to_dict()}), 200


@shops_bp.route("/<shop_uuid>", methods=["GET"])
def update_shop(shop_uuid: str):
    """
    exercise 3: view the shop details
    """
    uid = request.headers.get("uid")

    # todo: can user view the shop
    #       only staff an owners can view inactive shops

    with Session(current_app.engine) as s:
        shop = s.query(Shop).filter(Shop.id == shop_uuid).first()
        return jsonify({"shop": shop.to_dict()}), 200


@shops_bp.route("/all_products", methods=["GET"])
def get_all_products():
    """
    exercise 4: get all active products across all active shops
    """
    uid = request.headers.get("uid")

    # todo: use list or query interface (depending on who we are will depend on what
    #       we can see)

    with Session(current_app.engine) as s:
        # todo: add filter here
        #       can also do sorts, pagination, etc.
        products = s.query(Product).filter().all()
        return jsonify({"products": [product.to_dict() for product in products]}), 200


@shops_bp.route("/<shop_uuid>/products", methods=["GET"])
def get_products_in_shop(shop_uuid: str):
    """
    exercise 5: get all products in a shop
    """
    uid = request.headers.get("uid")

    # todo: what products can the user view (list)
    #       only staff and owner can view inactive products
    with Session(current_app.engine) as s:
        # add list filter here
        products = s.query(Product).filter().all()
        return jsonify({"products": [product.to_dict() for product in products]}), 200


@shops_bp.route("/<shop_id>/product", methods=["POST"])
def add_product_to_shop(shop_id: str):
    """
    exercise 6: add a product to a shop
    """
    uid = request.headers.get("uid")

    # todo: is user allowed to add new product to a shop?

    data = request.json
    product_name = data.get("product_name")
    product_desc = data.get("product_desc")
    product_price = float(data.get("product_price"))
    product_quantity = int(data.get("product_quantity"))
    product_active = bool(data.get("product_active"))

    with Session(current_app.engine) as s:
        shop = s.query(Shop).filter().first()
        product = Product(
            name=product_name,
            description=product_desc,
            price=product_price,
            quantity=product_quantity,
            is_active=product_active,
        )
        shop.products.append(product)
        s.update(shop)
        s.commit()
        return jsonify({"product added": product.to_dict()}), 200
