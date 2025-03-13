from api.core import db

class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.BIGINT, primary_key=True)
    product_id = db.Column(db.BIGINT, db.ForeignKey("product.id"), nullable=False)
    parent_id = db.Column(db.BIGINT, db.ForeignKey("review.id"), nullable=False)
    title = db.Column(db.VARCHAR, nullable=False)
    rating = db.Column(db.INT, nullable=False)
