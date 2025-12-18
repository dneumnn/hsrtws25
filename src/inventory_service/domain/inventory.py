"""Inventory domain model for the inventory service."""

from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Inventory(BaseModel):
    """Represents inventory status for a product."""

    id: UUID = Field(default_factory=uuid4)
    product_id: UUID
    warehouse_quantity: int = Field(default=0, ge=0)
    in_transit_quantity: int = Field(default=0, ge=0)
    expected_arrival_date: Optional[date] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    location: str = "main_warehouse"

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
        else:
            return "out_of_stock"

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "product_id": "550e8400-e29b-41d4-a716-446655440000",
                "warehouse_quantity": 10,
                "in_transit_quantity": 5,
                "expected_arrival_date": "2025-12-25",
                "location": "main_warehouse",
            }
        }
