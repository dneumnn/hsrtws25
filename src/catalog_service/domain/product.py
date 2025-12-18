"""Product domain model for the catalog service."""
from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, HttpUrl


class Product(BaseModel):
    """Represents a designer furniture product."""
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., max_length=255)
    description: str
    price: float = Field(..., gt=0)
    category: str = Field(..., pattern=r"^(chair|table|sofa|storage|lighting|other)$")
    style: str
    specifications: dict = Field(default_factory=dict)
    images: List[HttpUrl] = Field(..., min_items=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Eames Lounge Chair",
                "description": "Iconic mid-century modern lounge chair",
                "price": 5999.99,
                "category": "chair",
                "style": "modern",
                "specifications": {
                    "dimensions": "84cm x 84cm x 84cm",
                    "materials": "Rosewood, leather",
                    "weight": "45kg"
                },
                "images": ["https://example.com/eames.jpg"],
                "is_active": True
            }
        }
