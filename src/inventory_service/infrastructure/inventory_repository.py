"""Inventory repository implementation."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.inventory_service.domain.inventory import Inventory
from src.shared_kernel.infrastructure.repository import BaseRepository


class InventoryRepository(BaseRepository[Inventory]):
    """Repository for Inventory entities."""

    def __init__(self, db: Session):
        super().__init__(Inventory, db)

    def get_by_product_id(self, product_id: UUID) -> Optional[Inventory]:
        """Get inventory by product ID."""
        return self.db.query(Inventory).filter(Inventory.product_id == product_id).first()

    def get_in_stock_products(self, limit: int = 100) -> List[Inventory]:
        """Get products with inventory in stock."""
        return self.db.query(Inventory).filter(Inventory.warehouse_quantity > 0).limit(limit).all()

    def get_low_stock_products(self, threshold: int = 5) -> List[Inventory]:
        """Get products with low inventory."""
        return self.db.query(Inventory).filter(Inventory.warehouse_quantity <= threshold).all()

    def update_quantity(self, inventory_id: UUID, warehouse_quantity: int, in_transit_quantity: int) -> Optional[Inventory]:
        """Update inventory quantities."""
        inventory = self.get(inventory_id)
        if inventory:
            inventory.warehouse_quantity = warehouse_quantity
            inventory.in_transit_quantity = in_transit_quantity
            self.db.commit()
            self.db.refresh(inventory)
        return inventory
