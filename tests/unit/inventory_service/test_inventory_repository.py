"""Unit tests for Inventory repository."""

from unittest.mock import Mock
from uuid import uuid4
from inventory_service.infrastructure.inventory_orm import InventoryORM
from inventory_service.infrastructure.inventory_repository import InventoryRepository

def test_inventory_repository_get_by_product_id():
    """Test getting inventory by product ID."""
    mock_db = Mock()
    repo = InventoryRepository(mock_db)

    # Mock the database query
    mock_inventory = InventoryORM(
        id=uuid4(),
        product_id=uuid4(),
        warehouse_quantity=10,
        in_transit_quantity=5,
        location="main_warehouse",
    )

    mock_db.query.return_value.filter.return_value.first.return_value = mock_inventory

    result = repo.get_by_product_id(mock_inventory.product_id)

    assert result == mock_inventory


def test_inventory_repository_get_in_stock_products():
    """Test getting in-stock products."""
    mock_db = Mock()
    repo = InventoryRepository(mock_db)

    # Mock the database query
    mock_inventories = [
        InventoryORM(
            id=uuid4(),
            product_id=uuid4(),
            warehouse_quantity=10,
            in_transit_quantity=5,
            location="main_warehouse",
        ),
        InventoryORM(
            id=uuid4(),
            product_id=uuid4(),
            warehouse_quantity=5,
            in_transit_quantity=0,
            location="main_warehouse",
        ),
    ]

    mock_db.query.return_value.filter.return_value.limit.return_value.all.return_value = mock_inventories

    result = repo.get_in_stock_products(10)

    assert len(result) == 2
    assert result == mock_inventories


def test_inventory_repository_update_quantity():
    """Test updating inventory quantities."""
    mock_db = Mock()
    repo = InventoryRepository(mock_db)

    # Mock the database operations
    mock_inventory = InventoryORM(
        id=uuid4(),
        product_id=uuid4(),
        warehouse_quantity=10,
        in_transit_quantity=5,
        location="main_warehouse",
    )

    mock_db.query.return_value.filter.return_value.first.return_value = mock_inventory
    mock_db.commit = Mock()
    mock_db.refresh = Mock()

    result = repo.update_quantity(mock_inventory.id, 15, 3)

    assert result.warehouse_quantity == 15
    assert result.in_transit_quantity == 3
    assert mock_db.commit.called
    assert mock_db.refresh.called
