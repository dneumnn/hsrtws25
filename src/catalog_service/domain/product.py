"""Product domain model for the catalog service."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from urllib.parse import urlparse
from uuid import UUID, uuid4
import re

@dataclass
class Product:
    """Represents a designer furniture product."""

    name: str
    description: str
    price: float
    category: str
    style: str
    image: str = field(default_factory=str)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True

    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        if len(self.name) > 255:
            raise ValueError("name must be at most 255 characters")

        if self.price <= 0:
            raise ValueError("price must be greater than 0")

        if not re.match(r"^(chair|table|sofa|storage|lighting|other)$", self.category):
            raise ValueError("invalid category")

        if self.image:
            parsed = urlparse(self.image)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f"invalid URL: {self.image}")


