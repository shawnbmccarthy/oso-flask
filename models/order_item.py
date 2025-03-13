from api.core import db

class OrderItem(db.Model):
    __tablename__ = "order_item"

    id = db.Column(db.BIGINT, primary_key=True)
    product_id = db.Column(db.BIGINT, db.ForeignKey("product.id"), nullable=True)
    order_id = db.Column(db.BIGINT, db.ForeignKey("order.id"), nullable=True)
    sku = db.Column(db.VARCHAR(100), nullable=False)
    price = db.Column(db.FLOAT, nullable=False)
    discount = db.Column(db.FLOAT, nullable=False)
    quantity = db.Column(db.INT, nullable=False)