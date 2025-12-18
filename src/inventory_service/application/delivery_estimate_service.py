"""Delivery estimate application service."""
from typing import Optional
from uuid import UUID
from datetime import datetime
from src.inventory_service.domain.delivery_estimate import DeliveryEstimate
from src.inventory_service.infrastructure.inventory_repository import InventoryRepository


class DeliveryEstimateService:
    """Application service for delivery estimate operations."""

    def __init__(self, inventory_repository: InventoryRepository):
        self.inventory_repository = inventory_repository

    def calculate_delivery_estimate(self, product_id: UUID) -> Optional[DeliveryEstimate]:
        """Calculate delivery estimate for a product."""
        inventory = self.inventory_repository.get_by_product_id(product_id)
        if not inventory:
            return None

        if inventory.warehouse_quantity > 0:
            # Items in warehouse: 1-3 business days
            return DeliveryEstimate(
                product_id=product_id,
                location_type="warehouse",
                shipping_method="standard",
                destination_region="domestic",
                min_days=1,
                max_days=3
            )
        elif inventory.in_transit_quantity > 0 and inventory.expected_arrival_date:
            # Items in transit: expected arrival + 1-3 business days
            days_until_arrival = (inventory.expected_arrival_date - datetime.now().date()).days
            return DeliveryEstimate(
                product_id=product_id,
                location_type="in_transit",
                shipping_method="standard",
                destination_region="domestic",
                min_days=days_until_arrival + 1,
                max_days=days_until_arrival + 3
            )
        else:
            # Out of stock: no estimate
            return None

    def get_delivery_estimate_text(self, product_id: UUID) -> str:
        """Get human-readable delivery estimate text."""
        estimate = self.calculate_delivery_estimate(product_id)
        if estimate:
            return estimate.estimate_text
        return "Currently unavailable"
