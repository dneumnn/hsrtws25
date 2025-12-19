"""Unit tests for Inventory API endpoints."""

from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from uuid import uuid4
from src.inventory_service.presentation.api.inventory import (
    router,
    get_inventory_service,
)
from src.inventory_service.application.inventory_service import InventoryService


def test_get_inventory():
    """Test getting inventory by product ID."""
    # Create test client
    client = TestClient(router)

    # Mock the inventory service
    mock_service = Mock(spec=InventoryService)
    mock_inventory = Mock()
    mock_inventory.product_id = uuid4()
    mock_inventory.warehouse_quantity = 10
    mock_inventory.in_transit_quantity = 5
    mock_inventory.location = "main_warehouse"

    mock_service.get_inventory.return_value = mock_inventory

    with patch(
        "src.inventory_service.presentation.api.inventory.get_inventory_service",
        return_value=mock_service,
    ):
        response = client.get(f"/{mock_inventory.product_id}")

    assert response.status_code == 200
    assert response.json()["warehouse_quantity"] == 10


def test_get_inventory_not_found():
    """Test getting inventory for non-existent product."""
    # Create test client
    client = TestClient(router)

    # Mock the inventory service
    mock_service = Mock(spec=InventoryService)
    mock_service.get_inventory.return_value = None

    with patch(
        "src.inventory_service.presentation.api.inventory.get_inventory_service",
        return_value=mock_service,
    ):
        response = client.get(f"/{uuid4()}")

    assert response.status_code == 404


def test_get_all_inventory():
    """Test getting all inventory records."""
    # Create test client
    client = TestClient(router)

    # Mock the inventory service
    mock_service = Mock(spec=InventoryService)
    mock_inventories = [
        Mock(product_id=uuid4(), warehouse_quantity=10),
        Mock(product_id=uuid4(), warehouse_quantity=5),
    ]
    mock_service.get_all_inventory.return_value = mock_inventories

    with patch(
        "src.inventory_service.presentation.api.inventory.get_inventory_service",
        return_value=mock_service,
    ):
        response = client.get("/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_inventory():
    """Test updating inventory quantities."""
    # Create test client
    client = TestClient(router)

    # Mock the inventory service
    mock_service = Mock(spec=InventoryService)
    mock_inventory = Mock()
    mock_inventory.id = uuid4()
    mock_inventory.warehouse_quantity = 15
    mock_inventory.in_transit_quantity = 3

    mock_service.update_inventory.return_value = mock_inventory

    with patch(
        "src.inventory_service.presentation.api.inventory.get_inventory_service",
        return_value=mock_service,
    ):
        response = client.put(
            f"/{mock_inventory.id}?warehouse_quantity=15&in_transit_quantity=3"
        )

    assert response.status_code == 200
    assert response.json()["warehouse_quantity"] == 15


def test_create_inventory():
    """Test creating new inventory record."""
    # Create test client
    client = TestClient(router)

    # Mock the inventory service
    mock_service = Mock(spec=InventoryService)
    mock_inventory = Mock()
    mock_inventory.product_id = uuid4()
    mock_inventory.warehouse_quantity = 10
    mock_inventory.in_transit_quantity = 5

    mock_service.create_inventory.return_value = mock_inventory

    with patch(
        "src.inventory_service.presentation.api.inventory.get_inventory_service",
        return_value=mock_service,
    ):
        response = client.post(
            f"/{mock_inventory.product_id}?warehouse_quantity=10&in_transit_quantity=5"
        )

    assert response.status_code == 201
    assert response.json()["warehouse_quantity"] == 10
