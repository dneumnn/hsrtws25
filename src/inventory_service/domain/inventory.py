"""Inventory domain model for the inventory service."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class Inventory:
    """Represents inventory status for a product."""

    product_id: UUID
    warehouse_quantity: int = 0
    in_transit_quantity: int = 0
    expected_arrival_date: Optional[date] = None
    location: str = "main_warehouse"

    id: UUID = field(default_factory=uuid4)
    last_updated: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if self.warehouse_quantity < 0:
            raise ValueError("warehouse_quantity must be >= 0")
        if self.in_transit_quantity < 0:
            raise ValueError("in_transit_quantity must be >= 0")

    @property
    def available_quantity(self) -> int:
        """Calculate total available quantity."""
        return self.warehouse_quantity + self.in_transit_quantity

    @property
    def status(self) -> str:
        """Determine inventory status."""
        if self.warehouse_quantity > 0:
            return "in_stock"
        elif self.in_transit_quantity > 0:
            return "pre_order"
        return "out_of_stock"
