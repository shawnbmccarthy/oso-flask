from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID
from .base import Base, product_tag_table
import uuid

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    products: Mapped[list["Product"]] = relationship(
        "Product",
        secondary=product_tag_table,
        back_populates="tags",
    )
