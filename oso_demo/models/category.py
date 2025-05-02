from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID
from typing import Dict
from .base import Base, product_category_table
import uuid

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    products: Mapped[list["Product"]] = relationship(
        "Product",
        secondary=product_category_table,
        back_populates="categories",
    )

    def to_dict(self) -> Dict:
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())
