# Domain Event Bus and Message Handling
# Event-driven architecture for cross-service communication

from typing import Dict, Any, List
from uuid import uuid4
from datetime import datetime


# Domain event base class
class DomainEvent:
    """Base domain event class"""

    def __init__(self, event_type: str, data: Dict[str, Any]):
        self.event_id = str(uuid4())
        self.event_type = event_type
        self.timestamp = datetime.utcnow()
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
        }


# Domain event bus
class DomainEventBus:
    """Domain event bus for event-driven architecture"""

    def __init__(self):
        self.events: List[DomainEvent] = []
        self.handlers: Dict[str, List] = {}

    def publish(self, event):
        """Publish domain event"""
        self.events.append(event)

        # Notify handlers
        if event.event_type in self.handlers:
            for handler in self.handlers[event.event_type]:
                handler(event)

    def subscribe(self, event_type: str, handler):
        """Subscribe to domain events"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler):
        """Unsubscribe from domain events"""
        if event_type in self.handlers:
            self.handlers[event_type].remove(handler)

    def get_events(self) -> List[DomainEvent]:
        """Get all events"""
        return self.events

    def clear_events(self):
        """Clear all events"""
        self.events.clear()


# Message handler base class
class MessageHandler:
    """Base message handler class"""

    def __init__(self, event_bus: DomainEventBus):
        self.event_bus = event_bus

    def handle(self, event: DomainEvent):
        """Handle domain event"""
        raise NotImplementedError("handle method must be implemented")


# Global domain event bus instance
domain_event_bus = DomainEventBus()


# Example event handlers
class InventoryUpdatedHandler(MessageHandler):
    """Handler for inventory updated events"""

    def __init__(self):
        super().__init__(domain_event_bus)
        domain_event_bus.subscribe("inventory.updated", self.handle)

    def handle(self, event: DomainEvent):
        """Handle inventory updated event"""
        print(f"Inventory updated: {event.data}")
        # Add your inventory update logic here


class OrderCreatedHandler(MessageHandler):
    """Handler for order created events"""

    def __init__(self):
        super().__init__(domain_event_bus)
        domain_event_bus.subscribe("order.created", self.handle)

    def handle(self, event: DomainEvent):
        """Handle order created event"""
        print(f"Order created: {event.data}")
        # Add your order creation logic here
