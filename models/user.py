import bcrypt

from api.core import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.BIGINT, primary_key=True)
    first_name = db.Column(db.VARCHAR(50), nullable=False)
    email = db.Column(db.VARCHAR(50), nullable=False)
    password = db.Column(db.VARCHAR(128), nullable=False)
    admin = db.Column(db.INT, nullable=False)
    vendor = db.Column(db.INT, nullable=False)

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))