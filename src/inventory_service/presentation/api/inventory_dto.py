from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from uuid import UUID

# allows InventoryRead.model_validate(inventory_domain_object)
class InventoryRead(BaseModel):
    id: UUID
    product_id: UUID
    warehouse_quantity: int
    in_transit_quantity: int
    expected_arrival_date: Optional[date]
    last_updated: datetime
    location: str
    available_quantity: int
    status: str

    class Config:
        from_attributes = True

