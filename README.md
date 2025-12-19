# Designer Furniture Web Shop

This project implements a designer furniture web shop using Domain-Driven Design (DDD) principles with FastAPI, SQLAlchemy, and SQLite.

## Project Structure

The project follows a DDD structure with bounded contexts:

```text
src/
  catalog_service/
    domain/
    application/
    infrastructure/
    presentation/
  basket_service/
    domain/
    application/
    infrastructure/
    presentation/
  order_service/
    domain/
    application/
    infrastructure/
    presentation/
  inventory_service/
    domain/
    application/
    infrastructure/
    presentation/
  shared_kernel/
    domain/
    application/
    infrastructure/
  presentation/
    web/
    api/
    cli/
```

## Setup

1. Install Python 3.12+
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Running the Application

```bash
# Start FastAPI server
uvicorn app.main:app --reload --app-dir src
```

The application will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## Features

- Product catalog with search and filtering
- Real-time inventory management
- Shopping basket functionality
- Checkout process with payment integration
- Delivery estimate calculation

## Testing

```bash
# Run tests
pytest tests/
```

## Development

Follow the DDD patterns and maintain separation of concerns between bounded contexts.

## DDD Constitution

### 1. Domain First

The **domain model** is the primary source of truth.

- Business concepts, rules, and invariants take precedence over technical concerns.
- The system MUST reflect how domain experts think and speak.
- Technical abstractions MUST NOT distort or replace domain concepts.

### 2. Ubiquitous Language

A single, shared language MUST be used consistently across:

- Specifications
- Code
- Tests
- Documentation
- Conversations

### 3. Explicit Boundaries

The system is composed of **Bounded Contexts**.

- Each bounded context has:
  - Its own model
  - Its own language
  - Clear responsibilities
- Models MUST NOT leak across boundaries.
- Integration between contexts MUST be explicit and documented.

### 4. Model Integrity

Each domain model MUST protect its own invariants.

- Invariants MUST be enforced at the model level.
- Invalid states MUST be unrepresentable where possible.
- Business rules MUST NOT be scattered across layers.

### 5. Aggregates as Consistency Boundaries

Aggregates define transactional and consistency boundaries.

### 6. Behavior Over Data

Domain objects represent **behavior**, not just structure.

- Entities and Value Objects SHOULD encapsulate logic.
- Anemic domain models are considered a design failure.
- Business decisions belong in the domain, not orchestration layers.

## Test

Add pytest.ini

```text
[pytest]
pythonpath = src
```

The starlette.testclient module requires the httpx package to be installed.

## OR Mapping and Domain Model

Use dataclasses.dataclass for domain models, SQLAlchemy for persistence, and Pydantic for validation/serialization at the edges.

This keeps business rules inside the domain model, not in a validation framework.

API (Pydantic)
   ↓
Application Services
   ↓
Domain Models (dataclasses)
   ↓
Repositories
   ↓
SQLAlchemy ORM


Unused code:

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