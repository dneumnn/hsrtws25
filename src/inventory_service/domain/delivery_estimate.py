"""Delivery estimate domain model for the inventory service."""
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class DeliveryEstimate(BaseModel):
    """Represents delivery estimate for a product."""
    id: UUID = Field(default_factory=uuid4)
    product_id: UUID
    location_type: str = Field(..., pattern=r"^(warehouse|in_transit)$")
    shipping_method: str = "standard"
    destination_region: str = "domestic"
    min_days: int = Field(..., ge=1)
    max_days: int = Field(..., ge=1)
    calculated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def estimate_text(self) -> str:
        """Generate human-readable delivery estimate."""
        if self.min_days == self.max_days:
            return f"{self.min_days} business days"
        else:
            return f"{self.min_days}-{self.max_days} business days"

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "product_id": "550e8400-e29b-41d4-a716-446655440000",
                "location_type": "warehouse",
                "shipping_method": "standard",
                "destination_region": "domestic",
                "min_days": 1,
                "max_days": 3
            }
        }
