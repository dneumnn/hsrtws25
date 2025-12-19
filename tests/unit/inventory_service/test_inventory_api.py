"""Unit tests for Inventory API endpoints."""

from unittest.mock import Mock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from uuid import uuid4

from inventory_service.presentation.api.inventory_router import router
from inventory_service.presentation.api.inventory_router import get_inventory_service
from inventory_service.application.inventory_service import InventoryService

from inventory_service.domain.inventory import Inventory

def test_get_inventory():
    """Test getting inventory by product ID."""
    # Create test client
    #FIX: Correct approach: wrap the router in a FastAPI app:
    app = FastAPI()
    app.include_router(router)

    # Mock the inventory service
    mock_service = Mock(spec=InventoryService)

    mock_inventory = Inventory(
        id=uuid4(),
        product_id=uuid4(),
        warehouse_quantity=10,
        in_transit_quantity=5,
        location="main_warehouse",
    )

    mock_service.get_inventory.return_value = mock_inventory
    
    app.dependency_overrides[get_inventory_service] = lambda: mock_service

    client = TestClient(app)

    response = client.get(f"/inventory/{mock_inventory.product_id}")

    assert response.status_code == 200
    assert response.json()["warehouse_quantity"] == 10


def test_get_inventory_not_found():
    """Test getting inventory for non-existent product."""
    # Create test client
    #FIX: Correct approach: wrap the router in a FastAPI app:
    app = FastAPI()
    app.include_router(router)

    # Mock the inventory service
    mock_service = Mock(spec=InventoryService)
    mock_service.get_inventory.return_value = None

    app.dependency_overrides[get_inventory_service] = lambda: mock_service

    client = TestClient(app)

    response = client.get(f"/inventory/{uuid4()}")

    assert response.status_code == 404


def test_get_all_inventory():
    """Test getting all inventory records."""
    # Create test client
    #FIX: Correct approach: wrap the router in a FastAPI app:
    app = FastAPI()
    app.include_router(router)

    

    # Mock the inventory service
    mock_service = Mock(spec=InventoryService)
    mock_inventories = [
        Inventory(
            id=uuid4(),
            product_id=uuid4(),
            warehouse_quantity=10,
            in_transit_quantity=5,
            location="main_warehouse",
            ),
        Inventory(
            id=uuid4(),
            product_id=uuid4(),
            warehouse_quantity=5,
            in_transit_quantity=5,
            location="main_warehouse",
            )
    ]
    mock_service.get_all_inventory.return_value = mock_inventories
    app.dependency_overrides[get_inventory_service] = lambda: mock_service

    client = TestClient(app)
    response = client.get("/inventory/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_inventory():
    """Test updating inventory quantities."""
    # Create test client
    #FIX: Correct approach: wrap the router in a FastAPI app:
    app = FastAPI()
    app.include_router(router)

    # Mock the inventory service
    mock_service = Mock(spec=InventoryService)
    mock_inventory = Inventory(
        id=uuid4(),
        product_id=uuid4(),
        warehouse_quantity=15,
        in_transit_quantity=3,
        location="main_warehouse",
        )

    mock_service.update_inventory.return_value = mock_inventory
    app.dependency_overrides[get_inventory_service] = lambda: mock_service

    client = TestClient(app)

    with patch(
        "inventory_service.presentation.api.inventory_router.get_inventory_service",
        return_value=mock_service,
    ):
        response = client.put(
            f"/inventory/{mock_inventory.id}?warehouse_quantity=15&in_transit_quantity=3"
        )

    assert response.status_code == 200
    assert response.json()["warehouse_quantity"] == 15


def test_create_inventory():
    """Test creating new inventory record."""
    # Create test client
    #FIX: Correct approach: wrap the router in a FastAPI app:
    app = FastAPI()
    app.include_router(router)

    client = TestClient(app)

    # Mock the inventory service
    mock_service = Mock(spec=InventoryService)
    mock_inventory = Inventory(
        id=uuid4(),
        product_id=uuid4(),
        warehouse_quantity=10,
        in_transit_quantity=3,
        location="main_warehouse",
        )

    mock_service.create_inventory.return_value = mock_inventory

    app.dependency_overrides[get_inventory_service] = lambda: mock_service

    client = TestClient(app)

    response = client.post(
            f"/inventory/{mock_inventory.product_id}?warehouse_quantity=10&in_transit_quantity=5"
        )

    assert response.status_code == 201
    assert response.json()["warehouse_quantity"] == 10
