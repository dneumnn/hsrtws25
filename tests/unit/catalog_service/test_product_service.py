"""Unit tests for Product application service."""

from unittest.mock import Mock, patch
from uuid import uuid4
from pydantic import HttpUrl
from src.catalog_service.application.product_service import ProductService
from src.catalog_service.infrastructure.product_repository import ProductRepository


def test_product_service_get_product():
    """Test getting a product by ID."""
    mock_repo = Mock(spec=ProductRepository)
    service = ProductService(mock_repo)

    # Mock the repository and database
    mock_product = Mock()
    mock_product.id = uuid4()
    mock_product.name = "Test Product"

    mock_db = Mock()
    mock_repo.get.return_value = mock_product

    with patch(
        "src.catalog_service.application.product_service.get_db",
        return_value=[mock_db].__iter__(),
    ):
        result = service.get_product(mock_product.id)

    assert result == mock_product
    mock_repo.get.assert_called_once_with(mock_db, mock_product.id)


def test_product_service_get_all_products():
    """Test getting all active products."""
    mock_repo = Mock(spec=ProductRepository)
    service = ProductService(mock_repo)

    # Mock the repository and database
    mock_products = [Mock(), Mock()]
    mock_db = Mock()
    mock_repo.get_active_products.return_value = mock_products

    with patch(
        "src.catalog_service.application.product_service.get_db",
        return_value=[mock_db].__iter__(),
    ):
        result = service.get_all_products(50)

    assert len(result) == 2
    assert result == mock_products
    mock_repo.get_active_products.assert_called_once_with(mock_db, 50)


def test_product_service_search_products():
    """Test searching products."""
    mock_repo = Mock(spec=ProductRepository)
    service = ProductService(mock_repo)

    # Mock the repository and database
    mock_products = [Mock(), Mock()]
    mock_db = Mock()
    mock_repo.search.return_value = mock_products

    with patch(
        "src.catalog_service.application.product_service.get_db",
        return_value=[mock_db].__iter__(),
    ):
        result = service.search_products("test", 25)

    assert len(result) == 2
    assert result == mock_products
    mock_repo.search.assert_called_once_with(mock_db, "test", 25)


def test_product_service_create_product():
    """Test creating a new product."""
    mock_repo = Mock(spec=ProductRepository)
    service = ProductService(mock_repo)

    # Mock the repository and database
    product_data = {
        "name": "New Product",
        "description": "New Description",
        "price": 150.0,
        "category": "sofa",
        "style": "modern",
        "specifications": {},
        "images": [HttpUrl("https://example.com/new.jpg")],
    }

    mock_created_product = Mock()
    mock_created_product.id = uuid4()
    mock_created_product.name = "New Product"

    mock_db = Mock()
    mock_repo.create.return_value = mock_created_product

    with patch(
        "src.catalog_service.application.product_service.get_db",
        return_value=[mock_db].__iter__(),
    ):
        result = service.create_product(product_data)

    assert result == mock_created_product
    mock_repo.create.assert_called_once()
