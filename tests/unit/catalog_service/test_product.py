"""Unit tests for Product domain model."""

from datetime import datetime
from uuid import uuid4

from catalog_service.domain.product import Product


def test_product_creation():
    """Test creating a valid product."""

    product_data = {
        "name": "Eames Lounge Chair",
        "description": "Iconic mid-century modern lounge chair",
        "price": 5999.99,
        "category": "chair",
        "style": "modern",
        "image": "https://example.com/eames.jpg",
        "is_active": True,
    }

    product = Product(**product_data)

    assert product.id is not None
    assert product.name == "Eames Lounge Chair"
    assert product.price == 5999.99
    assert product.category == "chair"
    assert product.is_active is True


def test_product_validation():
    """Test product validation rules."""
    # Test invalid price
    try:
        Product(
            name="Test",
            description="Test",
            price=-100,
            category="chair",
            style="modern",
            image="https://example.com/test.jpg",
        )
        assert False, "Should have raised validation error for negative price"
    except ValueError:
        pass

    # Test invalid category
    try:
        Product(
            name="Test",
            description="Test",
            price=100,
            category="invalid_category",
            style="modern",
            image="https://example.com/test.jpg",
        )
        assert False, "Should have raised validation error for invalid category"
    except ValueError:
        pass

def test_product_timestamps():
    """Test product timestamp fields."""
    product = Product(
        name="Test",
        description="Test",
        price=100,
        category="chair",
        style="modern",
        image="https://example.com/test.jpg",
    )

    assert product.created_at is not None
    assert product.updated_at is not None
    assert isinstance(product.created_at, datetime)
    assert isinstance(product.updated_at, datetime)
