from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, func, UUID
from typing import Dict
from .base import Base, shop_employee_table
import uuid

class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), default=func.now(), onupdate=func.now())

    owner: Mapped["User"] = relationship("User", back_populates="shops")
    employees: Mapped[list["User"]] = relationship("User", secondary=shop_employee_table, back_populates="works_at")
    products: Mapped[list["Product"]] = relationship("Product", back_populates="shop", cascade="all, delete-orphan")

    def to_dict(self) -> Dict:
        return dict((col, getattr(self, col)) for col in self.__table__.columns.keys())