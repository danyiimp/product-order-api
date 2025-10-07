from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.item import Item


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("category.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    parent: Mapped["Category | None"] = relationship(
        remote_side="Category.id", back_populates="children", init=False
    )
    children: Mapped[list["Category"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan",
        single_parent=True,
        init=False,
    )
    items: Mapped[list["Item"]] = relationship(
        "Item", back_populates="category", init=False
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name}, parent_id={self.parent_id})>"
