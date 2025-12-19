"""Product repository implementation."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from dataclasses import asdict

from shared_kernel.infrastructure.repository import BaseRepository
from catalog_service.domain.product import Product
from catalog_service.infrastructure.product_orm import ProductORM


class ProductRepository(BaseRepository[ProductORM]):
    """Repository for Product entities."""

    def from_orm(self, product: ProductORM) -> Product:
        return Product(
            name=product.name,
            description=product.description,
            price=product.price,
            style=product.style,
            image=product.image,
            category=product.category,
            created_at=product.created_at,
            updated_at=product.updated_at,
            is_active=product.is_active,
            id=product.id
        )

    def from_orm_as_list(self, products: List[ProductORM]) -> List[Product]:
        return [self.from_orm(p) for p in products]

    def to_orm(product: Product) -> ProductORM:
        return ProductORM(**asdict(product))

    def __init__(self, db: Session):
        super().__init__(ProductORM, db)

    def get_by_name(self, name: str) -> Optional[Product]:
        """Get product by name."""
        return self.db.query(ProductORM).filter(ProductORM.name == name).first()

    def get_by_category(
        self, category: str, limit: int = 100
    ) -> List[Product]:
        """Get products by category."""
        products = self.db.query(ProductORM).\
            filter(ProductORM.category == category).\
            filter(ProductORM.is_active).limit(limit).all()
        return self.from_orm_as_list(products)

    def search(self, search_term: str, limit: int = 100) -> List[Product]:
        """Search products by name or description."""
        search_pattern = f"%{search_term}%"
        products = (
            self.db.query(ProductORM)
            .filter(
                or_(
                    ProductORM.name.ilike(search_pattern),
                    ProductORM.description.ilike(search_pattern)
                )
            )
            .filter(ProductORM.is_active)
            .limit(limit)
            .all()
        )
        return self.from_orm_as_list(products)

    def get_active_products(self, limit: int = 100) -> List[Product]:
        """Get all active products."""
        products = self.db.query(Product).filter(Product.is_active).limit(limit).all()
        return self.from_orm_as_list(products)
