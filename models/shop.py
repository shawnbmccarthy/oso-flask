from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, func, UUID
from .base import Base
import uuid

class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), default=func.now(), onupdate=func.now())

    owner: Mapped["User"] = relationship("User", back_populates="shops")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="shop", cascade="all, delete-orphan")