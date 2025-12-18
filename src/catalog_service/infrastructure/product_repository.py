"""Product repository implementation."""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_
from src.catalog_service.domain.product import Product


class ProductRepository:
    """Repository for Product entities."""

    def __init__(self, db: Session):
        self.db = db
        self.model = Product

    def get(self, db: Session, id: UUID) -> Optional[Product]:
        """Get entity by ID"""
        return db.query(self.model).filter(self.model.id == str(id)).first()

    def get_all(self, db: Session) -> List[Product]:
        """Get all entities"""
        return db.query(self.model).all()

    def create(self, db: Session, entity_data: dict) -> Product:
        """Create new entity"""
        entity = self.model(**entity_data)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def update(self, db: Session, id: UUID, update_data: dict) -> Optional[Product]:
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

    def get_by_name(self, db: Session, name: str) -> Optional[Product]:
        """Get product by name."""
        return db.query(Product).filter(Product.name == name).first()

    def get_by_category(
        self, db: Session, category: str, limit: int = 100
    ) -> List[Product]:
        """Get products by category."""
        return (
            db.query(Product)
            .filter(Product.category == category)
            .filter(Product.is_active)
            .limit(limit)
            .all()
        )

    def search(self, db: Session, search_term: str, limit: int = 100) -> List[Product]:
        """Search products by name or description."""
        search_pattern = f"%{search_term}%"
        return (
            db.query(Product)
            .filter(
                or_(
                    Product.name.ilike(search_pattern),
                    Product.description.ilike(search_pattern)
                )
            )
            .filter(Product.is_active)
            .limit(limit)
            .all()
        )

    def get_active_products(self, db: Session, limit: int = 100) -> List[Product]:
        """Get all active products."""
        return db.query(Product).filter(Product.is_active).limit(limit).all()
