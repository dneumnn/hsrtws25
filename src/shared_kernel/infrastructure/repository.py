# Repository Patterns and Unit of Work for DDD
# Data access patterns implementation

from typing import Dict, Any, List, Optional, Type
from uuid import UUID
from sqlalchemy.orm import Session
from pydantic import BaseModel


# Base repository interface
class BaseRepository:
    """Base repository interface"""

    def __init__(self, model: Type):
        self.model = model

    def get(self, db: Session, id: UUID) -> Optional[Any]:
        """Get entity by ID"""
        return db.query(self.model).filter(self.model.id == str(id)).first()

    def get_all(self, db: Session) -> List[Any]:
        """Get all entities"""
        return db.query(self.model).all()

    def create(self, db: Session, entity_data: Dict[str, Any]) -> Any:
        """Create new entity"""
        entity = self.model(**entity_data)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def update(
        self, db: Session, id: UUID, update_data: Dict[str, Any]
    ) -> Optional[Any]:
        """Update existing entity"""
        entity = self.get(db, id)
        if entity:
            for key, value in update_data.items():
                setattr(entity, key, value)
            db.commit()
            db.refresh(entity)
        return entity

    def delete(self, db: Session, id: UUID) -> bool:
        """Delete entity"""
        entity = self.get(db, id)
        if entity:
            db.delete(entity)
            db.commit()
            return True
        return False


# Unit of work interface
class UnitOfWork:
    """Unit of work interface"""

    def __init__(self, db: Session):
        self.db = db
        self.committed = False
        self.rolled_back = False

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
        if not self.committed and not self.rolled_back:
            self.db.commit()
            self.committed = True

    def rollback(self):
        """Rollback unit of work"""
        if not self.rolled_back and not self.committed:
            self.db.rollback()
            self.rolled_back = True


# Generic repository factory
class RepositoryFactory:
    """Factory for creating repositories"""

    @staticmethod
    def create_repository(model: Type) -> BaseRepository:
        """Create repository for given model"""
        return BaseRepository(model)
