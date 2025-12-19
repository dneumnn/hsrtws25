"""Unit tests for Product API endpoints."""

from unittest.mock import Mock, patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from uuid import uuid4
from pydantic import HttpUrl
from catalog_service.presentation.api.products import router, get_product_service
from catalog_service.application.product_service import ProductService
from catalog_service.domain.product import Product


def test_get_products():
    """Test getting all products."""

    app = FastAPI()
    app.include_router(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)
    mock_products = [
        Product(name = "Product 1",
                description = "Test Description 1",
                price = 100.0,
                category = "chair",
                style = "modern",
                image = "https://example.com/test.jpg",
                is_active=True,
                ),
        Product(name = "Product 2",
                description = "Test Description 2",
                price = 120.0,
                category = "chair",
                style = "modern",
                image = "https://example.com/test.jpg",
                is_active=True,
                )]
    mock_service.get_all_products.return_value = mock_products

    app.dependency_overrides[get_product_service] = lambda: mock_service

    client = TestClient(app)
    response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_product_by_id():
    """Test getting a product by ID."""

    app = FastAPI()
    app.include_router(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)

    mock_product = Product(name = "Test Product",
                           description = "Test Description",
                           price = 100.0,
                           category = "chair",
                           style = "modern",
                           image = "https://example.com/test.jpg",
                           is_active=True,
                           )

    mock_service.get_product.return_value = mock_product

    app.dependency_overrides[get_product_service] = lambda: mock_service

    client = TestClient(app)
    response = client.get(f"/products/{mock_product.id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

def test_get_product_not_found():
    """Test getting a non-existent product."""

    app = FastAPI()
    app.include_router(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)
    mock_service.get_product.return_value = None

    app.dependency_overrides[get_product_service] = lambda: mock_service

    client = TestClient(app)
    response = client.get(f"/products/{uuid4()}")


    assert response.status_code == 404

def test_create_product():
    """Test creating a new product."""

    app = FastAPI()
    app.include_router(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)
    mock_product = Product(name = "New Product",
                           description = "New Description",
                           price = 150.0,
                           category = "sofa",
                           style = "modern",
                           image = "https://example.com/new.jpg",
                           is_active=True,
                           )

    mock_service.create_product.return_value = mock_product

    product_data = {
        "name": "New Product",
        "description": "New Description",
        "price": 150.0,
        "category": "sofa",
        "style": "modern",
        "image": "https://example.com/new.jpg",
        "is_active": True,
    }

    app.dependency_overrides[get_product_service] = lambda: mock_service

    client = TestClient(app)
    response = client.post("/products", json=product_data)

    assert response.status_code == 201
    assert response.json()["name"] == "New Product"

def test_create_product_missing_fields():
    """Test creating a product with missing required fields."""
    
    app = FastAPI()
    app.include_router(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)

    product_data = {
        "name": "New Product",
        # Missing required fields
    }

    app.dependency_overrides[get_product_service] = lambda: mock_service

    client = TestClient(app)
    response = client.post("/products", json=product_data)

    assert response.status_code == 400
    assert "Missing required field" in response.json()["detail"]

def test_delete_product():
    """Test deleting a product."""

    app = FastAPI()
    app.include_router(router)

    # Mock the product service
    mock_service = Mock(spec=ProductService)
    mock_service.delete_product.return_value = True

    product_id = uuid4()

    app.dependency_overrides[get_product_service] = lambda: mock_service

    client = TestClient(app)
    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 204
