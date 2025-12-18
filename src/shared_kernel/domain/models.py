# Base Domain Models and Repository Patterns for DDD
# Core domain entities and value objects

from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from sqlalchemy.ext.declarative import declarative_base

# Base class for SQLAlchemy models
Base = declarative_base()


# Domain Events
class DomainEvent(BaseModel):
    """Base domain event"""

    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    data: dict


# Base Entity
class BaseEntity:
    """Base entity with common fields"""

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_timestamp(self):
        """Update entity timestamp"""
        self.updated_at = datetime.utcnow()


# Base Aggregate Root
class AggregateRoot(BaseEntity):
    """Base aggregate root for DDD"""

    domain_events: List[DomainEvent] = []

    def add_domain_event(self, event: DomainEvent):
        """Add domain event"""
        self.domain_events.append(event)

    def clear_domain_events(self):
        """Clear domain events"""
        self.domain_events = []


# Base Value Object
class ValueObject(BaseModel):
    """Base value object"""

    pass


# Repository Interface
class RepositoryInterface:
    """Repository interface for DDD"""

    def get(self, id: UUID):
        """Get entity by ID"""
        raise NotImplementedError

    def get_all(self):
        """Get all entities"""
        raise NotImplementedError

    def add(self, entity):
        """Add new entity"""
        raise NotImplementedError

    def update(self, entity):
        """Update existing entity"""
        raise NotImplementedError

    def delete(self, id: UUID):
        """Delete entity"""
        raise NotImplementedError


# Unit of Work Interface
class UnitOfWorkInterface:
    """Unit of work interface for DDD"""

    def __enter__(self):
        """Enter unit of work"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit unit of work"""
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    def commit(self):
        """Commit unit of work"""
        raise NotImplementedError

    def rollback(self):
        """Rollback unit of work"""
        raise NotImplementedError
