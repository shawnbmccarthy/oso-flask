from api.core import db

class ProductCategory(db.Model):
    __tablename__ = "product_category"

    id = db.Column(db.BIGINT, nullable=False, primary_key=True)
    product_id = db.Column(db.BIGINT, db.ForeignKey("product.id"), nullable=False)
    category_id = db.Column(db.BIGINT, db.ForeignKey("category.id"), nullable=False)