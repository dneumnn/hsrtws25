# Repository Patterns and Unit of Work for DDD
# Data access patterns implementation

from typing import Dict, Any, List, Optional
from typing import Generic, TypeVar, Type
from uuid import UUID
from sqlalchemy.orm import Session

T = TypeVar("T")

# Base repository interface
class BaseRepository(Generic[T]):
    """Base repository interface"""

    def __init__(self, model: Type[T], db: Session):
        self.db = db
        self.model = model

    def get(self, id: UUID) -> Optional[Any]:
        """Get entity by ID"""
        return self.db.query(self.model).filter(self.model.id == str(id)).first()

    def get_all(self, limit: int) -> List[Any]:
        """Get all entities"""
        return self.db.query(self.model).all()

    def create(self, entity_data: Dict[str, Any]) -> Any:
        """Create new entity"""
        entity = self.model(**entity_data)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(
        self, id: UUID, update_data: Dict[str, Any]
    ) -> Optional[Any]:
        """Update existing entity"""
        entity = self.get(id)
        if entity:
            for key, value in update_data.items():
                setattr(entity, key, value)
            self.db.commit()
            self.db.refresh(entity)
        return entity

    def delete(self, id: UUID) -> bool:
        """Delete entity"""
        entity = self.get(id)
        if entity:
            self.db.delete(entity)
            self.db.commit()
            return True
        return False

