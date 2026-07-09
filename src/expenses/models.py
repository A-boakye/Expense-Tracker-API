from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import date, datetime,timezone
from decimal import Decimal
from ..db.base import Base

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, func 
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from ..users.models import User
    


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(100))

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    category: Mapped[str] = mapped_column(String(50))

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    created_at: Mapped[datetime] = mapped_column(
       DateTime(timezone=True), default=datetime.now()
    )

    user: Mapped["User"] = relationship(
        back_populates="expenses"
    )