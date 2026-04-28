from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, func
from datetime import datetime
from typing import Optional


class Base(DeclarativeBase):
    __abstract__ = True  # Класс абстрактный, чтобы не создавать отдельную таблицу для него
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

class valsFull(Base):
    __tablename__ = 'val_dict'

    id: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment='Название валюты')
    eng_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='Англ. название валюты')
    nominal: Mapped[int]
    ParentCode: Mapped[str] = mapped_column(String(10), nullable=False, comment='Внутренний уникальный код валюты, которая являлась базовой(предыдущей) для данной валюты')
    ISO_Num_Code: Mapped[Optional[str]] = mapped_column(String(10))
    ISO_Char_Code: Mapped[Optional[str]] = mapped_column(String(10))