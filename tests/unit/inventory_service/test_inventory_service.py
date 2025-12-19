"""Unit tests for Inventory application service."""

from unittest.mock import Mock
from uuid import uuid4
from src.inventory_service.application.inventory_service import InventoryService
from src.inventory_service.infrastructure.inventory_repository import (
    InventoryRepository,
)


def test_inventory_service_get_inventory():
    """Test getting inventory by product ID."""
    mock_repo = Mock(spec=InventoryRepository)
    service = InventoryService(mock_repo)

    # Mock the repository
    mock_inventory = Mock()
    mock_inventory.product_id = uuid4()
    mock_inventory.warehouse_quantity = 10
    mock_inventory.in_transit_quantity = 5

    mock_repo.get_by_product_id.return_value = mock_inventory

    result = service.get_inventory(mock_inventory.product_id)

    assert result == mock_inventory
    mock_repo.get_by_product_id.assert_called_once_with(mock_inventory.product_id)


def test_inventory_service_get_in_stock_products():
    """Test getting in-stock products."""
    mock_repo = Mock(spec=InventoryRepository)
    service = InventoryService(mock_repo)

    # Mock the repository
    mock_inventories = [Mock(), Mock()]
    mock_repo.get_in_stock_products.return_value = mock_inventories

    result = service.get_in_stock_products(25)

    assert len(result) == 2
    assert result == mock_inventories
    mock_repo.get_in_stock_products.assert_called_once_with(25)


def test_inventory_service_update_inventory():
    """Test updating inventory quantities."""
    mock_repo = Mock(spec=InventoryRepository)
    service = InventoryService(mock_repo)

    # Mock the repository
    mock_inventory = Mock()
    mock_inventory.id = uuid4()
    mock_inventory.warehouse_quantity = 15
    mock_inventory.in_transit_quantity = 3

    mock_repo.update_quantity.return_value = mock_inventory

    result = service.update_inventory(mock_inventory.id, 15, 3)

    assert result == mock_inventory
    mock_repo.update_quantity.assert_called_once_with(mock_inventory.id, 15, 3)
