from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, func, UUID
from .base import Base
from typing import Dict
import uuid

class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_public: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), default=func.now(),onupdate=func.now())

    # relationships
    user: Mapped["User"] = relationship("User", back_populates="carts")
    items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    def to_dict(self) -> Dict:
        """
        gets relationship data
        """
        data = {col: getattr(self, col) for col in self.__table__.columns.keys()}
        data["user"] = self.user.to_dict() if self.user else None
        data["items"] = [item.to_dict() for item in self.items] if self.items else []
        return data
