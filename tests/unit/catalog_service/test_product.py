"""Unit tests for Product domain model."""

from datetime import datetime
from uuid import uuid4
from pydantic import HttpUrl
from catalog_service.domain.product import Product


def test_product_creation():
    """Test creating a valid product."""
    product_data = {
        "name": "Eames Lounge Chair",
        "description": "Iconic mid-century modern lounge chair",
        "price": 5999.99,
        "category": "chair",
        "style": "modern",
        "specifications": {
            "dimensions": "84cm x 84cm x 84cm",
            "materials": "Rosewood, leather",
            "weight": "45kg",
        },
        "images": [HttpUrl("https://example.com/eames.jpg")],
        "is_active": True,
    }

    product = Product(**product_data)

    assert product.id is not None
    assert product.name == "Eames Lounge Chair"
    assert product.price == 5999.99
    assert product.category == "chair"
    assert product.is_active is True
    assert len(product.images) == 1


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
            specifications={},
            images=[HttpUrl("https://example.com/test.jpg")],
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
            specifications={},
            images=[HttpUrl("https://example.com/test.jpg")],
        )
        assert False, "Should have raised validation error for invalid category"
    except ValueError:
        pass

    # Test missing images
    try:
        Product(
            name="Test",
            description="Test",
            price=100,
            category="chair",
            style="modern",
            specifications={},
            images=[],
        )
        assert False, "Should have raised validation error for empty images"
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
        specifications={},
        images=[HttpUrl("https://example.com/test.jpg")],
    )

    assert product.created_at is not None
    assert product.updated_at is not None
    assert isinstance(product.created_at, datetime)
    assert isinstance(product.updated_at, datetime)
