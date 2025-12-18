"""Product API endpoints for catalog service."""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from src.catalog_service.application.product_service import ProductService
from src.catalog_service.infrastructure.product_repository import ProductRepository
from src.catalog_service.domain.product import Product
from src.shared_kernel.infrastructure.database import get_db


router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}},
)


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Get product service dependency."""
    repository = ProductRepository(db)
    return ProductService(repository)


@router.get("/", response_model=List[Product])
def get_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(
        None, description="Search term for product name/description"
    ),
    limit: int = Query(100, description="Maximum number of products to return"),
    service: ProductService = Depends(get_product_service),
) -> List[Product]:
    """Get all products with optional filtering."""
    if category:
        return service.get_products_by_category(category, limit)
    elif search:
        return service.search_products(search, limit)
    else:
        return service.get_all_products(limit)


@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: UUID, service: ProductService = Depends(get_product_service)
) -> Product:
    """Get product details by ID."""
    product = service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=Product, status_code=201)
def create_product(
    product_data: dict, service: ProductService = Depends(get_product_service)
) -> Product:
    """Create a new product."""
    try:
        # Validate required fields
        required_fields = [
            "name",
            "description",
            "price",
            "category",
            "style",
            "images",
        ]
        for field in required_fields:
            if field not in product_data:
                raise HTTPException(
                    status_code=400, detail=f"Missing required field: {field}"
                )

        # Validate price
        if product_data["price"] <= 0:
            raise HTTPException(status_code=400, detail="Price must be positive")

        # Validate images
        if not product_data["images"] or len(product_data["images"]) == 0:
            raise HTTPException(
                status_code=400, detail="At least one image is required"
            )

        return service.create_product(product_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: UUID,
    product_data: dict,
    service: ProductService = Depends(get_product_service),
) -> Product:
    """Update an existing product."""
    try:
        product = service.update_product(product_id, product_data)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating product: {str(e)}")


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: UUID, service: ProductService = Depends(get_product_service)
) -> None:
    """Delete a product."""
    try:
        if not service.delete_product(product_id):
            raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting product: {str(e)}")
