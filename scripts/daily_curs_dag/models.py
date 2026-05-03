from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, func, Numeric, Date
from datetime import datetime, date
from typing import Optional
from decimal import Decimal


class Base(DeclarativeBase):
    __abstract__ = True  # Класс абстрактный, чтобы не создавать отдельную таблицу для него
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

class valsFull(Base):
    __tablename__ = 'daily_rates'

    vname:      Mapped[str] = mapped_column(String(200))
    vnom:       Mapped[int]
    vcurs:      Mapped[Decimal] = mapped_column(Numeric(18,6))
    vcode:      Mapped[str] = mapped_column(String(10), primary_key=True)
    vchcode:    Mapped[str] = mapped_column(String(3))
    vunitrate:  Mapped[Decimal] = mapped_column(Numeric(18,6))
    ondate:     Mapped[datetime] = mapped_column(primary_key=True)