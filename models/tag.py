from api.core import db

class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.INT, nullable=False, primary_key=True)
    title = db.Column(db.VARCHAR(75), nullable=False)
    slug = db.Column(db.VARCHAR(100), nullable=False)

    def __init__(self, title, slug, content):
        self.title = title
        self.slug = slug
        self.content = content

    def __repr__(self):
        return f"<Tag {self.id}:{self.title}>"