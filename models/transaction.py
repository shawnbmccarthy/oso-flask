from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Numeric, DateTime, func, UUID
from .base import Base
import uuid

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="mocked")  # pretend status
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    payment_id: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    order: Mapped["Order"] = relationship("Order", back_populates="transactions")