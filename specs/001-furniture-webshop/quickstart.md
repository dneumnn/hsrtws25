# Quickstart Guide: Designer Furniture Web Shop

## Prerequisites

- Python 3.12+
- Node.js 18+ (for frontend development)
- SQLite (included with Python)
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/furniture-webshop.git
cd furniture-webshop
```

### 2. Set Up Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your configuration

# Run database migrations
python -m alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### 3. Set Up Frontend

```bash
cd frontend

# Install dependencies (if using any build tools)
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Run Tests

```bash
# Backend tests
python -m pytest tests/

# Frontend tests (if applicable)
cd frontend
npm test
```

## Development Workflow

### Backend Development

- **Models**: Define in `backend/src/models/` using SQLAlchemy
- **Services**: Implement business logic in `backend/src/services/`
- **API Endpoints**: Create in `backend/src/api/` following REST conventions
- **Repositories**: Data access layer in `backend/src/repositories/`

### Frontend Development

- **Pages**: Create in `frontend/src/pages/`
- **Components**: Reusable components in `frontend/src/components/`
- **Services**: API communication in `frontend/src/services/`
- **Styles**: CSS files in `frontend/src/styles/`

### Database Management

```bash
# Create new migration
python -m alembic revision --autogenerate -m "description"

# Apply migrations
python -m alembic upgrade head

# Rollback migration
python -m alembic downgrade -1
```

## Key Features Implementation

### Product Catalog

- **Backend**: `GET /api/v1/products` endpoint
- **Frontend**: `src/pages/products.html` with search and filtering
- **Inventory**: Real-time availability from `GET /api/v1/inventory/{product_id}`

### Shopping Basket

- **Backend**: Basket management endpoints (`/api/v1/basket`)
- **Frontend**: `src/components/basket.js` with local storage fallback
- **Validation**: Real-time inventory checks before adding items

### Checkout Process

- **Backend**: Order creation endpoint (`POST /api/v1/checkout`)
- **Frontend**: Multi-step form in `src/pages/checkout.html`
- **Payment**: Integration with payment gateway (Stripe/PayPal)

### Delivery Estimates

- **Backend**: Calculation in `services/delivery_estimator.py`
- **Frontend**: Display in product cards and checkout summary
- **Logic**: Based on inventory location and shipping method

## API Endpoints Summary

### Products
- `GET /api/v1/products` - List all products
- `GET /api/v1/products/{id}` - Get product details
- `POST /api/v1/products` - Create product (Admin)

### Inventory
- `GET /api/v1/inventory/{product_id}` - Get inventory status

### Shopping Basket
- `GET /api/v1/basket` - Get current basket
- `POST /api/v1/basket` - Add item to basket
- `PUT /api/v1/basket/items/{id}` - Update item quantity
- `DELETE /api/v1/basket/items/{id}` - Remove item

### Orders
- `POST /api/v1/checkout` - Complete checkout
- `GET /api/v1/orders` - List user orders
- `GET /api/v1/orders/{id}` - Get order details

## Testing Strategy

### Unit Tests
- Backend: Test individual functions and services
- Frontend: Test utility functions and components

### Integration Tests
- Test API endpoints with real database
- Test frontend-backend communication

### End-to-End Tests
- Test complete user journeys (browsing → checkout)
- Test error scenarios and edge cases

## Deployment

### Local Development
```bash
# Backend
docker-compose up backend

# Frontend
docker-compose up frontend
```

### Production Deployment
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up --build

# Run migrations
docker-compose exec backend python -m alembic upgrade head
```

## Troubleshooting

### Common Issues

**Database connection errors**:
- Check `.env` file for correct database URL
- Ensure SQLite file has proper permissions

**CORS issues**:
- Verify FastAPI CORS middleware configuration
- Check frontend API base URL

**Inventory discrepancies**:
- Review transaction isolation in database
- Check for race conditions in basket operations

**Performance problems**:
- Add database indexes for frequently queried fields
- Implement caching for product catalog
- Optimize image loading on frontend