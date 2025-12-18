from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

# Import shared kernel infrastructure
from shared_kernel.infrastructure.database import init_db

# Create main FastAPI application
app = FastAPI(
    title="Designer Furniture Web Shop API",
    description="DDD-based e-commerce platform for designer furniture",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router registry for bounded contexts
routers: Dict[str, APIRouter] = {}

# Domain event bus for cross-context communication
domain_event_bus = []


def register_router(context_name: str, router: APIRouter):
    """
    Register a bounded context router
    """
    routers[context_name] = router
    app.include_router(router, prefix=f"/api/v1/{context_name}")


def publish_domain_event(event_name: str, event_data: Dict[str, Any]):
    """
    Publish domain events across bounded contexts
    """
    domain_event_bus.append({"event_name": event_name, "event_data": event_data})


# Initialize database on startup
@app.on_event("startup")
def on_startup():
    """
    Initialize database and other startup tasks
    """
    init_db()
    print("✅ Database initialized and ready")


# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Designer Furniture Web Shop",
        "version": "1.0.0",
    }


@app.get("/")
async def root():
    return {"message": "Designer Furniture Web Shop API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
