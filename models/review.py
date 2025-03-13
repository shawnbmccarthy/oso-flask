from api.core import Mixin
from oso_demo import db

class Review(db.Model):
    __tablename__ = "review"