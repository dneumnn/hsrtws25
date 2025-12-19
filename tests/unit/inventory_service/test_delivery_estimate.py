"""Unit tests for DeliveryEstimate domain model."""

from datetime import datetime
from uuid import uuid4
from src.inventory_service.domain.delivery_estimate import DeliveryEstimate


def test_delivery_estimate_creation():
    """Test creating a valid delivery estimate."""
    estimate_data = {
        "product_id": uuid4(),
        "location_type": "warehouse",
        "shipping_method": "standard",
        "destination_region": "domestic",
        "min_days": 1,
        "max_days": 3,
    }

    estimate = DeliveryEstimate(**estimate_data)

    assert estimate.id is not None
    assert estimate.product_id is not None
    assert estimate.location_type == "warehouse"
    assert estimate.min_days == 1
    assert estimate.max_days == 3
    assert estimate.estimate_text == "1-3 business days"


def test_delivery_estimate_text_generation():
    """Test delivery estimate text generation."""
    # Test same min/max days
    estimate = DeliveryEstimate(
        product_id=uuid4(), location_type="warehouse", min_days=2, max_days=2
    )
    assert estimate.estimate_text == "2 business days"

    # Test different min/max days
    estimate = DeliveryEstimate(
        product_id=uuid4(), location_type="warehouse", min_days=3, max_days=5
    )
    assert estimate.estimate_text == "3-5 business days"


def test_delivery_estimate_validation():
    """Test delivery estimate validation rules."""
    # Test invalid location_type
    try:
        DeliveryEstimate(
            product_id=uuid4(), location_type="invalid", min_days=1, max_days=3
        )
        assert False, "Should have raised validation error for invalid location_type"
    except ValueError:
        pass

    # Test invalid min_days
    try:
        DeliveryEstimate(
            product_id=uuid4(), location_type="warehouse", min_days=0, max_days=3
        )
        assert False, "Should have raised validation error for invalid min_days"
    except ValueError:
        pass


def test_delivery_estimate_timestamps():
    """Test delivery estimate timestamp fields."""
    estimate = DeliveryEstimate(
        product_id=uuid4(), location_type="warehouse", min_days=1, max_days=3
    )

    assert estimate.calculated_at is not None
    assert isinstance(estimate.calculated_at, datetime)
