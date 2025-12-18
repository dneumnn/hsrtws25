"""Inventory application service."""
from typing import List, Optional
from uuid import UUID
from src.inventory_service.domain.inventory import Inventory
from src.inventory_service.infrastructure.inventory_repository import InventoryRepository


class InventoryService:
    """Application service for inventory operations."""

    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def get_inventory(self, product_id: UUID) -> Optional[Inventory]:
        """Get inventory by product ID."""
        return self.repository.get_by_product_id(product_id)

    def get_all_inventory(self, limit: int = 100) -> List[Inventory]:
        """Get all inventory records."""
        return self.repository.get_all(limit)

    def update_inventory(self, inventory_id: UUID, warehouse_quantity: int, in_transit_quantity: int) -> Optional[Inventory]:
        """Update inventory quantities."""
        return self.repository.update_quantity(inventory_id, warehouse_quantity, in_transit_quantity)

    def create_inventory(self, product_id: UUID, warehouse_quantity: int = 0, in_transit_quantity: int = 0) -> Inventory:
        """Create new inventory record."""
        inventory = Inventory(
            product_id=product_id,
            warehouse_quantity=warehouse_quantity,
            in_transit_quantity=in_transit_quantity
        )
        return self.repository.create(inventory)

    def get_in_stock_products(self, limit: int = 100) -> List[Inventory]:
        """Get products with inventory in stock."""
        return self.repository.get_in_stock_products(limit)

    def get_low_stock_products(self, threshold: int = 5) -> List[Inventory]:
        """Get products with low inventory."""
        return self.repository.get_low_stock_products(threshold)
