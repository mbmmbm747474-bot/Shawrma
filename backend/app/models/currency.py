from sqlalchemy import Boolean, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class Currency(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    symbol: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    exchange_rate: Mapped[float] = mapped_column(
        Numeric(18, 6),
        default=1,
        nullable=False,
    )

    is_base: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Currency(code='{self.code}', symbol='{self.symbol}')>"
