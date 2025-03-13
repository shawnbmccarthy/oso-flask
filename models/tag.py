from oso_demo import db
from sqlalchemy.orm import Mapped, mapped_column

class Tag(db.Model):

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    title: Mapped[str]  = mapped_column(nullable=False)
    metaTitle: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Tag {self.id}:{self.title}>"