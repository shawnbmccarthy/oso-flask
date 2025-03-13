from api.core import db

class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.BIGINT, primary_key=True)
    product_id = db.Column(db.BIGINT, db.ForeignKey("product.id"), nullable=False)
    cart_id = db.Column(db.BIGINT, db.ForeignKey("cart.id"), nullable=False)
    sku = db.Column(db.VARCHAR(128), nullable=False)
    price = db.Column(db.FLOAT, nullable=False)
    discount = db.Column(db.FLOAT, nullable=False)
    quantity = db.Column(db.INT, nullable=False)