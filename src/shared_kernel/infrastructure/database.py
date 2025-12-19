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

'''
# Domain event tracking
domain_events = []


def register_domain_event(event_name: str, event_data: dict):
    """
    Register domain events for event-driven architecture
    """
    domain_events.append({"event_name": event_name, "event_data": event_data})


'''
