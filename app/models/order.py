from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.item import Item


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer.id", ondelete="CASCADE"), index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc), index=True
    )

    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="orders", init=False
    )
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        init=False,
    )

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, customer_id={self.customer_id})>"


class OrderItem(Base):
    __tablename__ = "order_item"

    order_id: Mapped[int] = mapped_column(
        ForeignKey("order.id", ondelete="CASCADE"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("item.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)

    order: Mapped["Order"] = relationship(
        "Order", back_populates="items", init=False
    )
    item: Mapped["Item"] = relationship("Item", init=False)

    def __repr__(self) -> str:
        return f"<OrderItem(order_id={self.order_id}, item_id={self.item_id}, quantity={self.quantity})>"
