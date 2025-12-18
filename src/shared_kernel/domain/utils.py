# Shared Utility Functions and Constants for DDD
# Common utilities used across bounded contexts

from typing import Dict, Any, List
from datetime import datetime
from uuid import UUID, uuid4


# Constants
class Constants:
    """Shared constants for the application"""

    # API endpoints
    API_BASE_URL = "/api/v1"

    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    # Date formats
    DATE_FORMAT = "%Y-%m-%d"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    # Error messages
    NOT_FOUND = "Resource not found"
    INVALID_INPUT = "Invalid input data"
    UNAUTHORIZED = "Unauthorized access"
    FORBIDDEN = "Forbidden"

    # Success messages
    SUCCESS = "Operation successful"
    CREATED = "Resource created successfully"
    UPDATED = "Resource updated successfully"
    DELETED = "Resource deleted successfully"


# Utility functions
class Utilities:
    """Shared utility functions"""

    @staticmethod
    def generate_uuid() -> UUID:
        """Generate UUID"""
        return uuid4()

    @staticmethod
    def current_timestamp() -> datetime:
        """Get current timestamp"""
        return datetime.utcnow()

    @staticmethod
    def format_date(date: datetime, date_format: str = Constants.DATE_FORMAT) -> str:
        """Format date"""
        return date.strftime(date_format)

    @staticmethod
    def parse_date(date_str: str, date_format: str = Constants.DATE_FORMAT) -> datetime:
        """Parse date string"""
        return datetime.strptime(date_str, date_format)

    @staticmethod
    def calculate_delivery_estimate(
        in_stock: bool, shipping_method: str = "standard"
    ) -> Dict[str, Any]:
        """Calculate delivery estimate"""
        if in_stock:
            if shipping_method == "express":
                return {"min_days": 1, "max_days": 2}
            else:
                return {"min_days": 3, "max_days": 5}
        else:
            if shipping_method == "express":
                return {"min_days": 5, "max_days": 7}
            else:
                return {"min_days": 7, "max_days": 14}

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @staticmethod
    def paginate_data(
        data: List[Any], page: int = 1, page_size: int = Constants.DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Paginate data"""
        start = (page - 1) * page_size
        end = start + page_size
        return {
            "data": data[start:end],
            "page": page,
            "page_size": page_size,
            "total": len(data),
            "total_pages": (len(data) + page_size - 1) // page_size,
        }


# Domain event utilities
class DomainEventUtilities:
    """Utilities for domain events"""

    @staticmethod
    def create_domain_event(event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create domain event"""
        return {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }

    @staticmethod
    def publish_domain_event(event: Dict[str, Any], event_bus: List[Dict[str, Any]]):
        """Publish domain event to event bus"""
        event_bus.append(event)

    @staticmethod
    def handle_domain_events(event_bus: List[Dict[str, Any]]):
        """Handle domain events from event bus"""
        for event in event_bus:
            print(f"Processing domain event: {event['event_type']}")
            # Add your event handling logic here
        event_bus.clear()
