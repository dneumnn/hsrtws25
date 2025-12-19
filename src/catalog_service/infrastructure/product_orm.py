# persistence/product_orm.py
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import Float, String, Date, UUID, Boolean
from uuid import UUID as PyUUID
from datetime import date
from typing import Optional

from shared_kernel.infrastructure.database import Base

class ProductORM(Base):
    __tablename__ = "product"

    id: Mapped[PyUUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True
        )
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    category: Mapped[str] = mapped_column(String)
    style: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)
    created_at: Mapped[date] = mapped_column(Date)
    updated_at: Mapped[date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean)
