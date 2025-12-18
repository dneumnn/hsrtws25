# API Documentation with Swagger UI
# FastAPI application with enhanced Swagger documentation

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import Dict, Any


# Custom OpenAPI schema
def custom_openapi(app: FastAPI):
    """Custom OpenAPI schema for Swagger UI"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Designer Furniture Web Shop API",
        version="1.0.0",
        description="DDD-based e-commerce platform for designer furniture",
        routes=app.routes,
    )

    # Add custom tags for bounded contexts
    openapi_schema["tags"] = [
        {
            "name": "catalog",
            "description": "Product catalog operations - Catalog Service bounded context",
        },
        {
            "name": "inventory",
            "description": "Inventory management operations - Inventory Service bounded context",
        },
        {
            "name": "basket",
            "description": "Shopping basket operations - Basket Service bounded context",
        },
        {
            "name": "order",
            "description": "Order processing operations - Order Service bounded context",
        },
        {"name": "auth", "description": "Authentication operations - Shared Kernel"},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Custom Swagger UI configuration
def configure_swagger_ui() -> Dict[str, Any]:
    """Configure Swagger UI settings"""
    return {
        "swagger_ui_parameters": {
            "docExpansion": "none",
            "persistAuthorization": True,
            "displayOperationId": True,
            "displayRequestDuration": True,
            "filter": True,
        }
    }
