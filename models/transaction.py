from api.core import db

class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.BIGINT, db.ForeignKey("user.id"), nullable=False)
    order_id = db.Column(db.BIGINT, db.ForeignKey("order.id"), nullable=False)
    code = db.Column(db.VARCHAR(100), nullable=False)
    type = db.Column(db.INT, nullable=False)
    mode = db.Column(db.INT, nullable=False)
    status = db.Column(db.INT, nullable=False)