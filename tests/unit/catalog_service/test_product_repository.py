"""Unit tests for Product repository."""

from unittest.mock import Mock, patch
from uuid import uuid4
from pydantic import HttpUrl
from src.catalog_service.domain.product import Product
from src.catalog_service.infrastructure.product_repository import ProductRepository


def test_product_repository_get():
    """Test getting a product by ID."""
    mock_db = Mock()
    repo = ProductRepository(mock_db)

    # Mock the database query
    mock_product = Product(
        id=uuid4(),
        name="Test Product",
        description="Test Description",
        price=100.0,
        category="chair",
        style="modern",
        specifications={},
        images=[HttpUrl("https://example.com/test.jpg")],
    )

    mock_db.query.return_value.filter.return_value.first.return_value = mock_product

    result = repo.get(mock_db, mock_product.id)

    assert result == mock_product


def test_product_repository_get_all():
    """Test getting all products."""
    mock_db = Mock()
    repo = ProductRepository(mock_db)

    # Mock the database query
    mock_products = [
        Product(
            id=uuid4(),
            name="Test Product 1",
            description="Test Description 1",
            price=100.0,
            category="chair",
            style="modern",
            specifications={},
            images=[HttpUrl("https://example.com/test1.jpg")],
        ),
        Product(
            id=uuid4(),
            name="Test Product 2",
            description="Test Description 2",
            price=200.0,
            category="table",
            style="modern",
            specifications={},
            images=[HttpUrl("https://example.com/test2.jpg")],
        ),
    ]

    mock_db.query.return_value.all.return_value = mock_products

    result = repo.get_all(mock_db)

    assert len(result) == 2
    assert result == mock_products


def test_product_repository_create():
    """Test creating a new product."""
    mock_db = Mock()
    repo = ProductRepository(mock_db)

    # Mock the database operations
    mock_product_data = {
        "name": "New Product",
        "description": "New Description",
        "price": 150.0,
        "category": "sofa",
        "style": "modern",
        "specifications": {},
        "images": [HttpUrl("https://example.com/new.jpg")],
    }

    mock_product = Product(**mock_product_data)

    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_product_model = Mock()
    mock_product_model.configure_mock(**mock_product_data)
    mock_db.add = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()

    with patch.object(Product, "__init__", return_value=None):
        result = repo.create(mock_db, mock_product_data)

    assert mock_db.add.called
    assert mock_db.commit.called
    assert mock_db.refresh.called


def test_product_repository_search():
    """Test searching products."""
    mock_db = Mock()
    repo = ProductRepository(mock_db)

    # Mock the database query
    mock_products = [
        Product(
            id=uuid4(),
            name="Search Product 1",
            description="Search Description 1",
            price=100.0,
            category="chair",
            style="modern",
            specifications={},
            images=[HttpUrl("https://example.com/search1.jpg")],
        )
    ]

    mock_db.query.return_value.filter.return_value.filter.return_value.limit.return_value.all.return_value = mock_products

    result = repo.search(mock_db, "Search", 10)

    assert len(result) == 1
    assert result == mock_products
