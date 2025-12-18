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
uvicorn app.main:app --reload
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

## Implementation Status

### Phase 1: Setup (Shared Infrastructure)

- [x] T001 Create DDD project structure with bounded contexts and shared kernel
- [ ] T002 Initialize Python 3.12+ project with FastAPI, SQLAlchemy, SQLite dependencies
- [ ] T003 [P] Configure linting and formatting tools (ruff, black)
- [ ] T004 [P] Setup pytest for testing
- [ ] T005 Create basic project documentation structure
- [ ] T006 Initialize git repository with proper .gitignore
- [ ] T007 Setup virtual environment and dependency management
- [ ] T008 [DDD] Create shared kernel structure in src/shared_kernel/
- [ ] T009 [DDD] Define domain events and shared interfaces

### Next Steps

1. Initialize Python project with dependencies
2. Configure development tools
3. Set up testing framework
4. Create shared kernel structure
