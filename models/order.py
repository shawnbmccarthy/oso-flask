from api.core import db

class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.BIGINT, primary_key=True)

    user_id = db.Column(db.BIGINT, db.ForeignKey("user.id"), nullable=True)
    session_id = db.Column(db.VARCHAR(100), nullable=False)
    status = db.Column(db.INT, nullable=False)
    sub_total = db.Column(db.FLOAT, nullable=False)
    item_discount = db.Column(db.FLOAT, nullable=False)
    tax = db.Column(db.FLOAT, nullable=False)
    shipping = db.Column(db.FLOAT, nullable=False)
    total = db.Column(db.FLOAT, nullable=False)
    promo = db.Column(db.VARCHAR(100), nullable=False)