# Error Handling and Logging Infrastructure for DDD
# Centralized error handling and logging setup

from typing import Dict, Any, Optional
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("furniture_webshop.log"),
    ],
)

logger = logging.getLogger("furniture_webshop")


# Custom exceptions
class DomainException(Exception):
    """Base domain exception"""

    def __init__(self, message: str, context: str = "Domain"):
        self.message = message
        self.context = context
        super().__init__(f"[{context}] {message}")


class ValidationException(DomainException):
    """Validation exception"""

    def __init__(self, message: str, field: str):
        super().__init__(message, f"Validation:{field}")
        self.field = field


class NotFoundException(DomainException):
    """Entity not found exception"""

    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(f"{entity_type} with ID {entity_id} not found", "NotFound")
        self.entity_type = entity_type
        self.entity_id = entity_id


class InventoryException(DomainException):
    """Inventory-related exception"""

    def __init__(self, message: str, product_id: str):
        super().__init__(message, "Inventory")
        self.product_id = product_id


# HTTP Exception handlers
async def domain_exception_handler(request: Request, exc: DomainException):
    """Handle domain exceptions"""
    logger.error(f"Domain Exception: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "DomainError",
            "message": exc.message,
            "context": exc.context,
        },
    )


async def validation_exception_handler(request: Request, exc: ValidationException):
    """Handle validation exceptions"""
    logger.error(f"Validation Exception: {exc.message} (field: {exc.field})")
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": exc.message,
            "field": exc.field,
        },
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException):
    """Handle not found exceptions"""
    logger.error(f"Not Found Exception: {exc.entity_type} with ID {exc.entity_id}")
    return JSONResponse(
        status_code=404,
        content={
            "error": "NotFound",
            "message": exc.message,
            "entity_type": exc.entity_type,
            "entity_id": exc.entity_id,
        },
    )


# Logging service
class LoggingService:
    """Centralized logging service"""

    def __init__(self, service_name: str = "furniture_webshop"):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)

    def info(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log info message"""
        if context:
            self.logger.info(f"{message} | {context}")
        else:
            self.logger.info(message)

    def error(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None,
    ):
        """Log error message"""
        if exception:
            self.logger.error(
                f"{message} | {context or {}} | Exception: {str(exception)}"
            )
        elif context:
            self.logger.error(f"{message} | {context}")
        else:
            self.logger.error(message)

    def debug(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log debug message"""
        if context:
            self.logger.debug(f"{message} | {context}")
        else:
            self.logger.debug(message)


# Error handling service
class ErrorHandlingService:
    """Centralized error handling service"""

    def __init__(self):
        self.logger = LoggingService("error_handler")

    def handle_exception(self, exception: Exception, context: str = "Unknown"):
        """Handle exceptions with logging and appropriate responses"""
        self.logger.error(f"Exception in {context}", {"exception": str(exception)})

        if isinstance(exception, DomainException):
            return {
                "error": "DomainError",
                "message": exception.message,
                "context": exception.context,
            }, 400

        elif isinstance(exception, ValidationException):
            return {
                "error": "ValidationError",
                "message": exception.message,
                "field": exception.field,
            }, 422

        elif isinstance(exception, NotFoundException):
            return {
                "error": "NotFound",
                "message": exception.message,
                "entity_type": exception.entity_type,
                "entity_id": exception.entity_id,
            }, 404

        else:
            return {
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "details": str(exception),
            }, 500
