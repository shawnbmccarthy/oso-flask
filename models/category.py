from api.core import db

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.BIGINT, primary_key=True)

    parent_id = db.Column(db.BIGINT, db.ForeignKey("category.id"), nullable=True)
    title = db.Column(db.VARCHAR(75), nullable=False)
    slug = db.Column(db.VARCHAR(100), nullable=False)