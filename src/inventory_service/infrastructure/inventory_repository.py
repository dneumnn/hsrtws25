"""Inventory repository implementation."""
from typing import List, Optional
from uuid import UUID
from dataclasses import asdict

from sqlalchemy.orm import Session


from shared_kernel.infrastructure.repository import BaseRepository

from inventory_service.domain.inventory import Inventory
from inventory_service.infrastructure.inventory_orm import InventoryORM

class InventoryRepository(BaseRepository[InventoryORM]):
    """Repository for Inventory entities."""

    def from_orm(self, inv: InventoryORM) -> Inventory:
        return Inventory(
            id=inv.id,
            product_id=inv.product_id,
            warehouse_quantity=inv.warehouse_quantity,
            in_transit_quantity=inv.in_transit_quantity,
            expected_arrival_date=inv.expected_arrival_date,
            location=inv.location,
            last_updated=inv.last_updated
        )
    
    
    def to_orm(inv: Inventory) -> InventoryORM:
        return InventoryORM(**asdict(inv))

    def __init__(self, db: Session):
        super().__init__(InventoryORM, db)

    def get_by_product_id(self, product_id: UUID) -> Optional[Inventory]:
        """Get inventory by product ID."""

        return self.db.query(InventoryORM).filter(InventoryORM.product_id == product_id).first()

    def get_in_stock_products(self, limit: int = 100) -> List[Inventory]:
        """Get products with inventory in stock."""
        return self.db.query(InventoryORM).filter(InventoryORM.warehouse_quantity > 0).limit(limit).all()

    def get_low_stock_products(self, threshold: int = 5) -> List[Inventory]:
        """Get products with low inventory."""
        return self.db.query(InventoryORM).filter(InventoryORM.warehouse_quantity <= threshold).all()

    def update_quantity(self, inventory_id: UUID, warehouse_quantity: int, in_transit_quantity: int) -> Optional[Inventory]:
        """Update inventory quantities."""
        inventoryORM = self.get(inventory_id)
        if inventoryORM:
            inventoryORM.warehouse_quantity = warehouse_quantity
            inventoryORM.in_transit_quantity = in_transit_quantity
            self.db.commit()
            self.db.refresh(inventoryORM)
        return self.from_orm(inventoryORM)
    


