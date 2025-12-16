# Data Model: Designer Furniture Web Shop

## Core Entities

### Product
```
- id: UUID (primary key)
- name: String (required, max 255 chars)
- description: Text (required)
- price: Decimal (required, > 0)
- category: String (required, enum: chair, table, sofa, storage, lighting, etc.)
- style: String (required)
- specifications: JSON (dimensions, materials, weight, etc.)
- images: List[URL] (required, min 1 image)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated)
- is_active: Boolean (default: true)
```

**Validation Rules**:
- Name must be unique within category
- Price must be positive
- At least one image required
- Category must be from predefined list

### Inventory
```
- id: UUID (primary key)
- product_id: UUID (foreign key, required)
- warehouse_quantity: Integer (default: 0, min: 0)
- in_transit_quantity: Integer (default: 0, min: 0)
- expected_arrival_date: Date (nullable, for in-transit items)
- last_updated: DateTime (auto-generated)
- location: String (warehouse identifier)
```

**Validation Rules**:
- Product must exist
- Quantities cannot be negative
- Expected arrival date required if in_transit_quantity > 0

**State Transitions**:
- warehouse_quantity decreases when orders are placed
- in_transit_quantity decreases when items arrive at warehouse
- warehouse_quantity increases when in-transit items arrive

### ShoppingBasket
```
- id: UUID (primary key)
- session_id: String (required, for guest users)
- user_id: UUID (foreign key, nullable for guests)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated)
- status: String (enum: active, abandoned, checked_out)
```

### BasketItem
```
- id: UUID (primary key)
- basket_id: UUID (foreign key, required)
- product_id: UUID (foreign key, required)
- quantity: Integer (required, min: 1)
- price_at_addition: Decimal (required, snapshot of product price)
- added_at: DateTime (auto-generated)
```

**Validation Rules**:
- Quantity must not exceed available inventory
- Product must be active
- Basket must be in 'active' status

### Order
```
- id: UUID (primary key)
- user_id: UUID (foreign key, required)
- order_number: String (unique, auto-generated)
- status: String (enum: pending, processing, shipped, delivered, cancelled)
- total_amount: Decimal (required, calculated)
- shipping_address: JSON (required)
- billing_address: JSON (required)
- payment_method: String (required)
- payment_status: String (enum: pending, paid, failed, refunded)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated)
```

**State Transitions**:
- pending → processing (when payment confirmed)
- processing → shipped (when items dispatched)
- shipped → delivered (when customer receives)
- Any state → cancelled (by customer or admin)

### OrderItem
```
- id: UUID (primary key)
- order_id: UUID (foreign key, required)
- product_id: UUID (foreign key, required)
- quantity: Integer (required, min: 1)
- price: Decimal (required, snapshot)
- product_name: String (snapshot)
- delivery_estimate: Date (calculated)
```

### Customer
```
- id: UUID (primary key)
- email: String (required, unique, email format)
- password_hash: String (required)
- first_name: String (required)
- last_name: String (required)
- phone: String (nullable)
- created_at: DateTime (auto-generated)
- last_login: DateTime (nullable)
- is_active: Boolean (default: true)
```

**Validation Rules**:
- Email must be unique and valid format
- Password must meet complexity requirements
- Phone must be valid format if provided

### DeliveryEstimate
```
- id: UUID (primary key)
- product_id: UUID (foreign key, required)
- location_type: String (enum: warehouse, in_transit)
- shipping_method: String (required)
- destination_region: String (required)
- min_days: Integer (required, min: 1)
- max_days: Integer (required, >= min_days)
- calculated_at: DateTime (auto-generated)
```

## Relationships

- **Product → Inventory**: One-to-One (product has inventory)
- **Product → BasketItem**: One-to-Many (product in many baskets)
- **Product → OrderItem**: One-to-Many (product in many orders)
- **ShoppingBasket → BasketItem**: One-to-Many (basket contains items)
- **ShoppingBasket → Customer**: Many-to-One (customer has baskets)
- **Order → OrderItem**: One-to-Many (order contains items)
- **Order → Customer**: Many-to-One (customer places orders)
- **Product → DeliveryEstimate**: One-to-Many (product has estimates for different scenarios)

## Domain Rules

1. **Inventory Management**:
   - Available quantity = warehouse_quantity + in_transit_quantity
   - Prevent overselling with database transactions
   - Update delivery estimates when inventory status changes

2. **Shopping Basket**:
   - Validate quantities against real-time inventory on addition
   - Revalidate basket before checkout
   - Clear basket after successful checkout

3. **Order Processing**:
   - Reserve inventory when order is placed
   - Release inventory if order is cancelled
   - Update delivery estimates based on actual shipping dates

4. **Product Availability**:
   - "In Stock" if warehouse_quantity > 0
   - "Available for pre-order" if in_transit_quantity > 0 and warehouse_quantity = 0
   - "Out of Stock" if both quantities = 0

5. **Delivery Estimation**:
   - Warehouse items: 1-3 business days
   - In-transit items: expected_arrival_date + shipping time
   - Update estimates when inventory location changes