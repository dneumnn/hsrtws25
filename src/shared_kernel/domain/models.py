# Shared Kernel Domain Models

from datetime import datetime

from pydantic import UUID4, BaseModel


class DomainEvent(BaseModel):
    """Base class for all domain events"""

    event_id: UUID4
    event_type: str
    timestamp: datetime
    payload: dict


class IntegrationEvent(BaseModel):
    """Base class for integration events between bounded contexts"""

    event_id: UUID4
    source_context: str
    destination_context: str
    timestamp: datetime
    payload: dict


class ValueObject(BaseModel):
    """Base class for value objects"""

    pass


class Entity(BaseModel):
    """Base class for entities"""

    id: UUID4


class AggregateRoot(Entity):
    """Base class for aggregate roots"""

    version: int = 0
    created_at: datetime
    updated_at: datetime


class SharedInterfaces:
    """Shared interfaces for cross-context communication"""

    pass
