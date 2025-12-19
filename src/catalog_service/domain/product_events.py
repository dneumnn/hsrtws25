# TODO
"""Product domain events for inventory changes."""
from datetime import datetime
from typing import Dict, Any
from uuid import UUID
from pydantic import BaseModel


#TODO - should be part of inventory ?
class ProductInventoryChangedEvent(BaseModel):
    """Event triggered when product inventory changes."""
    event_type: str = "product_inventory_changed"
    product_id: UUID
    old_quantity: int
    new_quantity: int
    timestamp: datetime = datetime.utcnow()
    metadata: Dict[str, Any] = {}

    def __str__(self):
        return f"ProductInventoryChangedEvent(product_id={self.product_id}, old_quantity={self.old_quantity}, new_quantity={self.new_quantity})"


class ProductCreatedEvent(BaseModel):
    """Event triggered when a new product is created."""
    event_type: str = "product_created"
    product_id: UUID
    product_name: str
    timestamp: datetime = datetime.utcnow()

    def __str__(self):
        return f"ProductCreatedEvent(product_id={self.product_id}, product_name={self.product_name})"


class ProductUpdatedEvent(BaseModel):
    """Event triggered when a product is updated."""
    event_type: str = "product_updated"
    product_id: UUID
    updated_fields: Dict[str, Any]
    timestamp: datetime = datetime.utcnow()

    def __str__(self):
        return f"ProductUpdatedEvent(product_id={self.product_id}, updated_fields={list(self.updated_fields.keys())})"


class ProductDeletedEvent(BaseModel):
    """Event triggered when a product is deleted."""
    event_type: str = "product_deleted"
    product_id: UUID
    product_name: str
    timestamp: datetime = datetime.utcnow()

    def __str__(self):
        return f"ProductDeletedEvent(product_id={self.product_id}, product_name={self.product_name})"
