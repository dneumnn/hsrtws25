"""Inventory API endpoints for inventory service."""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from inventory_service.application.inventory_service import InventoryService
from inventory_service.application.delivery_estimate_service import DeliveryEstimateService
from inventory_service.infrastructure.inventory_repository import InventoryRepository
from inventory_service.domain.inventory import Inventory
from shared_kernel.infrastructure.database import get_db


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
    responses={404: {"description": "Not found"}},
)


def get_inventory_service(db: Session = Depends(get_db)) -> InventoryService:
    """Get inventory service dependency."""
    repository = InventoryRepository(db)
    return InventoryService(repository)


def get_delivery_estimate_service(db: Session = Depends(get_db)) -> DeliveryEstimateService:
    """Get delivery estimate service dependency."""
    repository = InventoryRepository(db)
    return DeliveryEstimateService(repository)


@router.get("/{product_id}", response_model=Inventory)
def get_inventory(
    product_id: UUID,
    service: InventoryService = Depends(get_inventory_service)
) -> Inventory:
    """Get inventory status for a product."""
    inventory = service.get_inventory(product_id)
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found for product")
    return inventory


@router.get("/", response_model=List[Inventory])
def get_all_inventory(
    limit: int = Query(100, description="Maximum number of inventory records to return"),
    service: InventoryService = Depends(get_inventory_service)
) -> List[Inventory]:
    """Get all inventory records."""
    return service.get_all_inventory(limit)


@router.get("/{product_id}/delivery-estimate")
def get_delivery_estimate(
    product_id: UUID,
    service: DeliveryEstimateService = Depends(get_delivery_estimate_service)
) -> dict:
    """Get delivery estimate for a product."""
    estimate_text = service.get_delivery_estimate_text(product_id)
    return {
        "product_id": str(product_id),
        "delivery_estimate": estimate_text
    }


@router.put("/{inventory_id}", response_model=Inventory)
def update_inventory(
    inventory_id: UUID,
    warehouse_quantity: int = Query(..., description="Warehouse quantity"),
    in_transit_quantity: int = Query(..., description="In transit quantity"),
    service: InventoryService = Depends(get_inventory_service)
) -> Inventory:
    """Update inventory quantities."""
    inventory = service.update_inventory(inventory_id, warehouse_quantity, in_transit_quantity)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


@router.post("/{product_id}", response_model=Inventory, status_code=201)
def create_inventory(
    product_id: UUID,
    warehouse_quantity: int = Query(0, description="Initial warehouse quantity"),
    in_transit_quantity: int = Query(0, description="Initial in transit quantity"),
    service: InventoryService = Depends(get_inventory_service)
) -> Inventory:
    """Create new inventory record for a product."""
    return service.create_inventory(product_id, warehouse_quantity, in_transit_quantity)
