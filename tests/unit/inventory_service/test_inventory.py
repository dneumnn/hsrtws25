"""Unit tests for Inventory domain model."""

from datetime import date, datetime
from uuid import uuid4

from inventory_service.domain.inventory import Inventory


def test_inventory_creation():
    """Test creating a valid inventory record."""
    inventory_data = {
        "product_id": uuid4(),
        "warehouse_quantity": 10,
        "in_transit_quantity": 5,
        "expected_arrival_date": date(2025, 12, 25),
        "location": "main_warehouse",
    }

    inventory = Inventory(**inventory_data)

    assert inventory.id is not None
    assert inventory.product_id is not None
    assert inventory.warehouse_quantity == 10
    assert inventory.in_transit_quantity == 5
    assert inventory.available_quantity == 15
    assert inventory.status == "in_stock"


def test_inventory_status_calculation():
    """Test inventory status calculation."""
    # Test in_stock status
    inventory = Inventory(
        product_id=uuid4(), warehouse_quantity=10, in_transit_quantity=0
    )
    assert inventory.status == "in_stock"

    # Test pre_order status
    inventory = Inventory(
        product_id=uuid4(), warehouse_quantity=0, in_transit_quantity=5
    )
    assert inventory.status == "pre_order"

    # Test out_of_stock status
    inventory = Inventory(
        product_id=uuid4(), warehouse_quantity=0, in_transit_quantity=0
    )
    assert inventory.status == "out_of_stock"


def test_inventory_validation():
    """Test inventory validation rules."""
    # Test negative warehouse quantity
    try:
        Inventory(product_id=uuid4(), warehouse_quantity=-5, in_transit_quantity=0)
        assert False, (
            "Should have raised validation error for negative warehouse quantity"
        )
    except ValueError:
        pass

    # Test negative in_transit quantity
    try:
        Inventory(product_id=uuid4(), warehouse_quantity=0, in_transit_quantity=-5)
        assert False, (
            "Should have raised validation error for negative in_transit quantity"
        )
    except ValueError:
        pass


def test_inventory_timestamps():
    """Test inventory timestamp fields."""
    inventory = Inventory(
        product_id=uuid4(), warehouse_quantity=10, in_transit_quantity=5
    )

    assert inventory.last_updated is not None
    assert isinstance(inventory.last_updated, datetime)
