from api.core import db

class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.BIGINT, primary_key=True)
    session_id = db.Column(db.VARCHAR(128), nullable=False)
    token = db.Column(db.VARCHAR(128), nullable=False)
    status = db.Column(db.INT, nullable=False)

    user_id = db.Column(db.BIGINT, db.ForeignKey("user.id"), nullable=False)
