"""Product application service."""

from typing import List, Optional
from uuid import UUID
from src.catalog_service.domain.product import Product
from src.catalog_service.infrastructure.product_repository import ProductRepository
from src.shared_kernel.infrastructure.database import get_db
from src.shared_kernel.infrastructure.error_handling import LoggingService


class ProductService:
    """Application service for product operations."""

    def __init__(self, repository: ProductRepository):
        self.repository = repository
        self.logger = LoggingService("catalog_service")

    def get_product(self, product_id: UUID) -> Optional[Product]:
        """Get a product by ID."""
        self.logger.info(f"Getting product with ID: {product_id}")
        db = next(get_db())
        product = self.repository.get(db, product_id)
        if product:
            self.logger.debug(f"Product found: {product.name}")
        else:
            self.logger.debug(f"Product not found: {product_id}")
        return product

    def get_all_products(self, limit: int = 100) -> List[Product]:
        """Get all active products."""
        self.logger.info(f"Getting all active products (limit: {limit})")
        db = next(get_db())
        products = self.repository.get_active_products(db, limit)
        self.logger.debug(f"Found {len(products)} active products")
        return products

    def search_products(self, search_term: str, limit: int = 100) -> List[Product]:
        """Search products by name or description."""
        self.logger.info(
            f"Searching products with term: '{search_term}' (limit: {limit})"
        )
        db = next(get_db())
        products = self.repository.search(db, search_term, limit)
        self.logger.debug(f"Found {len(products)} products matching search")
        return products

    def get_products_by_category(
        self, category: str, limit: int = 100
    ) -> List[Product]:
        """Get products by category."""
        self.logger.info(f"Getting products by category: {category} (limit: {limit})")
        db = next(get_db())
        products = self.repository.get_by_category(db, category, limit)
        self.logger.debug(f"Found {len(products)} products in category {category}")
        return products

    def create_product(self, product_data: dict) -> Product:
        """Create a new product."""
        try:
            self.logger.info("Creating new product")
            db = next(get_db())
            product = Product(**product_data)
            created_product = self.repository.create(db, product.model_dump())
            self.logger.info(f"Product created successfully: {created_product.id}")
            return created_product
        except Exception as e:
            self.logger.error("Error creating product", {"error": str(e)})
            raise

    def update_product(self, product_id: UUID, product_data: dict) -> Optional[Product]:
        """Update an existing product."""
        try:
            self.logger.info(f"Updating product: {product_id}")
            db = next(get_db())
            product = self.repository.get(db, product_id)
            if product:
                updated_product = self.repository.update(db, product_id, product_data)
                self.logger.info(f"Product updated successfully: {product_id}")
                return updated_product
            else:
                self.logger.debug(f"Product not found for update: {product_id}")
                return None
        except Exception as e:
            self.logger.error(f"Error updating product {product_id}", {"error": str(e)})
            raise

    def delete_product(self, product_id: UUID) -> bool:
        """Delete a product."""
        try:
            self.logger.info(f"Deleting product: {product_id}")
            db = next(get_db())
            return self.repository.delete(db, product_id)
        except Exception as e:
            self.logger.error(f"Error deleting product {product_id}", {"error": str(e)})
            raise
