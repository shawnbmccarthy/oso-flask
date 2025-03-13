from api.core import db

class ProductTag(db.Model):
    __tablename__ = "product_tag"

    id = db.Column(db.BIGINT, nullable=False, primary_key=True)
    product_id = db.Column(db.BIGINT, db.ForeignKey("product.id"), nullable=False)
    tag_id = db.Column(db.BIGINT, db.ForeignKey("tag.id"), nullable=False)