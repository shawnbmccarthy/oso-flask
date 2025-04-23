from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Numeric, DateTime, func, UUID

from models import Category
from .base import Base, product_category_table, product_tag_table
import uuid

class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    shop_id: Mapped[str] = mapped_column(ForeignKey("shops.id"), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), default=func.now(), onupdate=func.now())

    shop: Mapped["Shop"] = relationship("Shop", back_populates="products")
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="product")
    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="product")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="product", cascade="all, delete-orphan")

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=product_tag_table,
        back_populates="products",
    )

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary=product_category_table,
        back_populates="products",
    )
