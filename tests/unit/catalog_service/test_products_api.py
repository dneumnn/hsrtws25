"""Unit tests for Product API endpoints."""

from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from uuid import uuid4
from pydantic import HttpUrl
from src.catalog_service.presentation.api.products import router, get_product_service
from src.catalog_service.application.product_service import ProductService


def test_get_products():
    """Test getting all products."""
    # Create test client
    client = TestClient(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)
    mock_products = [
        Mock(id=uuid4(), name="Product 1"),
        Mock(id=uuid4(), name="Product 2"),
    ]
    mock_service.get_all_products.return_value = mock_products

    with patch(
        "src.catalog_service.presentation.api.products.get_product_service",
        return_value=mock_service,
    ):
        response = client.get("/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_product_by_id():
    """Test getting a product by ID."""
    # Create test client
    client = TestClient(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)
    mock_product = Mock()
    mock_product.id = uuid4()
    mock_product.name = "Test Product"
    mock_product.description = "Test Description"
    mock_product.price = 100.0
    mock_product.category = "chair"
    mock_product.style = "modern"
    mock_product.specifications = {}
    mock_product.images = [HttpUrl("https://example.com/test.jpg")]
    mock_product.is_active = True

    mock_service.get_product.return_value = mock_product

    with patch(
        "src.catalog_service.presentation.api.products.get_product_service",
        return_value=mock_service,
    ):
        response = client.get(f"/{mock_product.id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"


def test_get_product_not_found():
    """Test getting a non-existent product."""
    # Create test client
    client = TestClient(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)
    mock_service.get_product.return_value = None

    with patch(
        "src.catalog_service.presentation.api.products.get_product_service",
        return_value=mock_service,
    ):
        response = client.get(f"/{uuid4()}")

    assert response.status_code == 404


def test_create_product():
    """Test creating a new product."""
    # Create test client
    client = TestClient(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)
    mock_product = Mock()
    mock_product.id = uuid4()
    mock_product.name = "New Product"

    mock_service.create_product.return_value = mock_product

    product_data = {
        "name": "New Product",
        "description": "New Description",
        "price": 150.0,
        "category": "sofa",
        "style": "modern",
        "specifications": {},
        "images": ["https://example.com/new.jpg"],
    }

    with patch(
        "src.catalog_service.presentation.api.products.get_product_service",
        return_value=mock_service,
    ):
        response = client.post("/", json=product_data)

    assert response.status_code == 201
    assert response.json()["name"] == "New Product"


def test_create_product_missing_fields():
    """Test creating a product with missing required fields."""
    # Create test client
    client = TestClient(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)

    product_data = {
        "name": "New Product",
        # Missing required fields
    }

    with patch(
        "src.catalog_service.presentation.api.products.get_product_service",
        return_value=mock_service,
    ):
        response = client.post("/", json=product_data)

    assert response.status_code == 400
    assert "Missing required field" in response.json()["detail"]


def test_delete_product():
    """Test deleting a product."""
    # Create test client
    client = TestClient(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)
    mock_service.delete_product.return_value = True

    product_id = uuid4()

    with patch(
        "src.catalog_service.presentation.api.products.get_product_service",
        return_value=mock_service,
    ):
        response = client.delete(f"/{product_id}")

    assert response.status_code == 204
