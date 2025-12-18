# Domain-Driven Design Database Infrastructure
# Shared kernel database setup for SQLite with SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database configuration
DATABASE_URL = "sqlite:///./furniture_webshop.db"

# Create SQLAlchemy engine
database_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)

# Base class for declarative models
Base = declarative_base()


# Dependency to get database session
def get_db():
    """
    Dependency to get database session for FastAPI endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize database tables
def init_db():
    """
    Initialize all database tables
    """
    Base.metadata.create_all(bind=database_engine)


# Domain event tracking
domain_events = []


def register_domain_event(event_name: str, event_data: dict):
    """
    Register domain events for event-driven architecture
    """
    domain_events.append({"event_name": event_name, "event_data": event_data})


# Repository base class for DDD patterns
class BaseRepository:
    """
    Base repository class implementing repository pattern
    """

    def __init__(self, model):
        self.model = model

    def get(self, db, id):
        """Get entity by ID"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db):
        """Get all entities"""
        return db.query(self.model).all()

    def create(self, db, entity_data):
        """Create new entity"""
        entity = self.model(**entity_data)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def update(self, db, id, update_data):
        """Update existing entity"""
        entity = self.get(db, id)
        if entity:
            for key, value in update_data.items():
                setattr(entity, key, value)
            db.commit()
            db.refresh(entity)
        return entity

    def delete(self, db, id):
        """Delete entity"""
        entity = self.get(db, id)
        if entity:
            db.delete(entity)
            db.commit()
        return entity
