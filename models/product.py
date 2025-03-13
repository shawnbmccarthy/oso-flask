from api.core import db
from sqlalchemy.dialects.postgresql import UUID, BIGINT, VARCHAR

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(BIGINT, primary_key=True)
    user_id = db.Column(BIGINT, db.ForeignKey('user.id'))
    title = db.Column(VARCHAR(100), nullable=False)
    slug = db.Column(VARCHAR(100), nullable=False)
    type = db.Column(db.INT, nullable=False)
    sku = db.Column(db.VARCHAR(100), nullable=False)
    price = db.Column(db.FLOAT, nullable=False)
    discount = db.Column(db.FLOAT, nullable=False)
    quantity = db.Column(db.INT, nullable=False)
    shop = db.Column(db.INT, nullable=False)