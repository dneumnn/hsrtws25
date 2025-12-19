# persistence/inventory_orm.py
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import Integer, String, Date, UUID
from uuid import UUID as PyUUID
from datetime import date
from typing import Optional

from shared_kernel.infrastructure.database import Base

class InventoryORM(Base):
    __tablename__ = "inventory"

    id: Mapped[PyUUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True
        )
    product_id: Mapped[PyUUID] = mapped_column(UUID)
    warehouse_quantity: Mapped[int] = mapped_column(Integer)
    in_transit_quantity: Mapped[int] = mapped_column(Integer)
    expected_arrival_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    location: Mapped[str] = mapped_column(String)
    last_updated: Mapped[date] = mapped_column(Date)
    