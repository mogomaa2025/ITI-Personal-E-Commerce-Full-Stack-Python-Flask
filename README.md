
## **README.md**

```markdown
# Flask E-Commerce API with UI
## Production-Ready with Enterprise Security

A complete e-commerce REST API built with Flask and JSON database, featuring **bcrypt password security**, **JWT token refresh mechanism**, **cart restoration**, and a modern web interface. Perfect for API testing, automation testing practice, and real-world applications.

### 🆕 **Latest Updates (v2.2)**
- ✅ **Bcrypt Password Hashing** - Production-grade security (12 rounds)
- ✅ **Token Refresh Mechanism** - 24h access + 30d refresh tokens
- ✅ **Cart Restoration** - Auto-restore items on order cancellation
- ✅ **Enhanced Security** - Admin registration protection, password validation
- ✅ **Workflow Validation** - Order status transitions enforced


## 🎯 Project Purpose

This project is designed specifically for:
- **API Testing Training** - 30+ REST API endpoints
- **Automation Testing Practice** - Selenium-ready UI with proper element IDs
- **Software Testing Graduation Projects** - Comprehensive testing scenarios
- **Learning Flask Development** - Clean, well-documented code

## ✨ Features

### 🆕 **v2.2 New Features (Production-Ready)**
- ✅ **Bcrypt Password Security** - Industry-standard hashing (12 rounds, production-ready)
- ✅ **Token Refresh Mechanism** - 24h access + 30d refresh tokens (OAuth 2.0 standard)
- ✅ **Cart Restoration** - Items auto-restored when order cancelled (smart quantity handling)
- ✅ **Enhanced Security** - Admin registration protection, password validation (6+ chars, 1 number, 1 letter)
- ✅ **Workflow Validation** - Order status transitions enforced (pending→processing→shipped→delivered)
- ✅ **Category Protection** - Cannot delete categories with products
- ✅ **Unlike Products** - New endpoint to remove likes

### Backend (REST API - 104+ Endpoints)
- ✅ **User Authentication** - JWT access + refresh tokens, bcrypt hashing
- ✅ **Product Management** - Full CRUD operations, bulk updates, inventory management
- ✅ **Shopping Cart** - Add, update, remove items with smart cart restoration
- ✅ **Order Processing** - Complete order lifecycle with status workflow validation
- ✅ **Product Reviews** - Rating and comment system with duplicate prevention
- ✅ **Admin Dashboard** - Statistics, analytics, user activity tracking
- ✅ **JSON Database** - No database setup required (75 products, 30 users, 50+ orders seeded)
- ✅ **CORS Enabled** - Ready for frontend integration

### Frontend (Web UI)
- ✅ **Responsive Design** - Works on all devices
- ✅ **User Registration/Login** - Complete authentication flow
- ✅ **Product Catalog** - Browse, search, and filter products
- ✅ **Shopping Cart** - Visual cart management
- ✅ **User Profile** - Profile viewing and editing
- ✅ **Order History** - Track and manage orders
- ✅ **Admin Panel** - Product and order management
- ✅ **Selenium-Ready** - All elements have unique IDs for automation

## 📋 API Endpoints Overview (104 total)

The API surface spans multiple feature groups organized into 18 main categories:

### Core Endpoints
- **Health Check** – `GET /api/health` – API status verification
- **System Health** – `GET /api/system/health` – Comprehensive system monitoring
- **API Docs** – `GET /api/docs` – Full API documentation

### Authentication & Users (6 endpoints)
- User registration, login, profile management, activity tracking
- JWT token-based authentication with role-based access (admin/user)

### Product Management (11 endpoints)
- Complete CRUD operations, bulk updates, inventory management
- Search, filtering by category, price range, pagination
- Product export functionality for admins

### Cart Management (5 endpoints)
- Add/update/remove items, view cart, clear cart
- Real-time item total and cart total calculations

### Order Management (8 endpoints)
- Create orders from cart, order history, status tracking
- Update shipping address, admin status updates, order cancellation

### Reviews & Ratings (3 endpoints)
- Create reviews with ratings (1-5 stars)
- Get product reviews with average rating
- Check if user has reviewed a product

### Product Likes (3 endpoints)
- Like/unlike products, count likes
- Check if user liked a product

### Categories (3 endpoints)
- List all categories, create new categories (admin)
- Delete categories with proper validation

### Admin & Statistics (7 endpoints)
- Dashboard statistics, low-stock alerts
- Stock management, bulk product updates
- User activity tracking, data exports

### Help & Support (4 endpoints)
- Help articles by category, get help categories
- Create help articles (admin), contact management

### Contact System (2 endpoints)
- Submit contact messages, view messages (admin)

### Wishlist System (3 endpoints)
- Get wishlist, add to wishlist, remove from wishlist

**Total Endpoints:** 104 curated requests organized in logical folders
**Authentication:** JWT token required for protected endpoints
**Response Format:** Consistent JSON structure with success/error handling

For detailed endpoint documentation, import `E-Commerce_API.postman_collection.json` into Postman.

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```
cd E-Commerce/g
```

### Step 2: Create Virtual Environment (Recommended)
```
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```
pip install -r requirements.txt
```

Required packages:
- Flask==3.0.0
- Flask-CORS==4.0.0
- PyJWT==2.8.0

### Step 4: Generate Test Data
```
python seed_data.py
```

This creates:
- **30 users** (1 admin + 1 test user + 28 regular users)
- **75 products** across 5 categories (Electronics, Clothing, Books, Home & Garden, Sports)
- **50 orders** with various statuses
- **100 product reviews** with ratings
- **20 active cart items**
- **5 categories** with descriptions

### Step 5: Run the Application
```
python app.py
```

The application will start on `http://localhost:5000`

## 🔐 Test Credentials

### Admin Account
```
Email: admin@test.com
Password: admin123
Access: Full admin dashboard, user management, product management
```

### Test User Account
```
Email: user@test.com
Password: user123
Access: Normal user features (browse, cart, orders, profile)
```

### Other Users
```
Password for all generated users: password123
Emails: Various (check data/users.json)
```

---

## 🆕 What's New in v2.2 - Important Changes

### 1. Token Refresh Mechanism (NEW)
**Login now returns TWO tokens:**
```json
{
  "token": "access_token...",        // Use for 24 hours
  "refresh_token": "refresh_token..."  // Use for 30 days
}
```

**How to use:**
- Use `token` (access token) for all API requests: `Authorization: Bearer {token}`
- When it expires after 24h, use refresh token to get a new one:
  ```
  POST /api/refresh
  Body: {"refresh_token": "your_refresh_token"}
  Response: {"token": "new_access_token"}
  ```

### 2. Cart Restoration (NEW)
**When you cancel an order, items automatically return to your cart!**
- Before: Items lost, had to re-add manually
- Now: Items automatically restored with correct quantities
- Works for both pending and processing orders

### 3. Enhanced Security (NEW)
- ✅ **Password Rules:** Minimum 6 characters, must have 1 number and 1 letter
- ✅ **Admin Protection:** Cannot register as admin (security fix)
- ✅ **Bcrypt Ready:** Production-grade password hashing available (`auth_bcrypt.py`)
- ✅ **Current:** Using SHA256 (fallback due to Windows bcrypt DLL issue)

### 4. Order Workflow Validation (NEW)
**Orders now follow proper status transitions:**
- pending → processing → shipped → delivered
- Can cancel from any status
- Cannot skip stages (e.g., pending → delivered blocked)

### 5. New Endpoint (NEW)
```
DELETE /api/products/likes/{like_id}  - Unlike a product
```

---

## ⚠️ Important Notes

### Windows Bcrypt Issue
If you see `ImportError: DLL load failed while importing _bcrypt`:
- **Current:** App uses SHA256 fallback (works fine for testing)
- **For Production:** Install Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe
- **Then:** Copy `auth_bcrypt.py` to `auth.py` and reseed data

### Testing the New Features
See [TESTCASES_API.md](TESTCASES_API.md) for 218+ test cases including 18 new tests for:
- Token refresh (7 tests)
- Cart restoration (8 tests)  
- Bcrypt security (3 tests)

## 📁 Project Structure

```
mysite/
│
├── 📄 Core Application Files
│   ├── app.py                      # Main Flask application (1561 lines)
│   │                              # - REST API endpoints (104+)
│   │                              # - Web interface routes
│   │                              # - Authentication & authorization
│   │                              # - Database initialization
│   ├── extended_api.py            # Extended API routes
│   │                              # - Help & FAQ system
│   │                              # - Contact & Support system
│   │                              # - Wishlist management
│   │                              # - Analytics endpoints
│   ├── config.py                  # Configuration settings
│   │                              # - JWT settings
│   │                              # - Data directory configuration
│   │                              # - Security keys
│   ├── auth.py                    # Authentication helpers
│   │                              # - JWT token generation/verification
│   │                              # - Password hashing (SHA256)
│   │                              # - Admin role validation
│   └── utils.py                   # Utility functions
│                                  # - JSON file operations
│                                  # - Data validation
│                                  # - ID generation
│                                  # - Email validation
│
├── 📊 Data Files (JSON Database)
│   └── data/
│       ├── users.json             # User accounts (30 test users)
│       ├── products.json          # Products catalog (75 products)
│       ├── orders.json            # Order records (50+ orders)
│       ├── cart.json              # Shopping cart items
│       ├── categories.json        # Product categories (5 categories)
│       ├── reviews.json           # Product reviews (100+ reviews)
│       ├── likes.json             # Product likes tracking
│       ├── wishlist.json          # User wishlists
│       ├── help.json              # Help articles & FAQs
│       ├── contact_messages.json  # Contact form submissions
│       ├── coupons.json           # Coupon codes
│       ├── notifications.json     # User notifications
│       ├── helpful_votes.json     # Helpful votes on articles
│       ├── blog_posts.json        # Blog content
│       ├── analytics.json         # Analytics & statistics
│       └── fail.json              # Failed transaction logs
│
├── 🎨 Templates (Jinja2 HTML - 16 templates)
│   └── templates/
│       ├── base.html              # Base template with navigation & layout
│       ├── index.html             # Home page with featured products
│       ├── login.html             # User login page
│       ├── register.html          # User registration page
│       ├── products.html          # Products listing with filters
│       ├── product_detail.html    # Individual product details
│       ├── cart.html              # Shopping cart page
│       ├── orders.html            # User order history
│       ├── profile.html           # User profile management
│       ├── admin.html             # Admin dashboard
│       ├── wishlist.html          # Wishlist management
│       ├── help.html              # Help & FAQ page
│       ├── contact.html           # Contact form page
│       ├── notifications.html     # Notifications page
│       ├── advanced_search.html   # Advanced product search
│       └── test_framework.html    # Testing framework page
│
├── 🎨 Static Files
│   └── static/
│       ├── css/
│       │   └── style.css          # Main stylesheet
│       ├── js/
│       │   └── main.js            # Main JavaScript utilities
│       └── img/
│           ├── placeholder.svg    # Placeholder images
│           └── i3ti.png           # Product images
│
├── 🔧 Maintenance & Utility Scripts
│   └── Cleanup-Maintenance Scripts/
│       ├── seed_data.py           # Generate 30 users, 75 products, 50 orders
│       ├── clear_data.py          # Clear all data files
│       ├── update_data.py         # Add more products to database
│       ├── fix_product_images.py  # Fix product image URLs
│       ├── cleanup_duplicate_likes.py  # Remove duplicate likes
│       ├── test_like_validation.py    # Validate like functionality
│       └── test_helpful_validation.py # Validate helpful votes
│
├── 📋 Documentation
│   ├── README.md                  # Project documentation (this file)
│   ├── POSTMAN.md                 # Postman collection guide (104 endpoints)
│   └── UPDATE_SUMMARY.md          # Update changelog
│
├── 📦 Dependencies
│   └── requirements.txt           # Python packages
│       ├── Flask==3.0.0
│       ├── Flask-CORS==4.0.0
│       └── PyJWT==2.8.0
│
└── __pycache__/                   # Python cache (auto-generated)
```

### 📊 Data Files Summary

| File | Purpose | Records | Status |
|------|---------|---------|--------|
| `users.json` | User accounts & authentication | 30 users | Seeded |
| `products.json` | Product catalog | 75 products | Seeded |
| `orders.json` | Order management | 50+ orders | Seeded |
| `categories.json` | Product categories | 5 categories | Pre-defined |
| `reviews.json` | Product reviews & ratings | 100+ reviews | Seeded |
| `likes.json` | Product likes | Auto-populated | Dynamic |
| `cart.json` | Shopping cart items | User-dependent | Dynamic |
| `wishlist.json` | User wishlists | User-dependent | Dynamic |
| `help.json` | Help articles & FAQs | Expandable | Dynamic |
| `contact_messages.json` | Contact form submissions | Dynamic | Dynamic |
| `notifications.json` | User notifications | Dynamic | Dynamic |
| `coupons.json` | Promotional codes | Expandable | Dynamic |
| `helpful_votes.json` | Help article votes | Dynamic | Dynamic |
| `blog_posts.json` | Blog content | Expandable | Dynamic |
| `analytics.json` | Analytics & statistics | Aggregate data | Dynamic |

### 🎯 Template Coverage (16 templates)

| Template | Purpose | Type | Features |
|----------|---------|------|----------|
| `base.html` | Layout & Navigation | Base | Header, nav, footer |
| `index.html` | Home page | Public | Featured products, hero |
| `login.html` | User authentication | Auth | Email, password login |
| `register.html` | New user signup | Auth | Registration form |
| `products.html` | Product listing | Public | Grid, filters, search |
| `product_detail.html` | Product info | Public | Details, reviews, likes |
| `cart.html` | Shopping cart | Protected | Item list, totals, checkout |
| `orders.html` | Order history | Protected | Order list, status, details |
| `profile.html` | User account | Protected | Profile edit, settings |
| `admin.html` | Admin dashboard | Admin | Stats, product management |
| `wishlist.html` | User wishlist | Protected | Saved products |
| `help.html` | Help & FAQ | Public | Help articles, search |
| `contact.html` | Contact form | Public | Support request submission |
| `notifications.html` | Notifications | Protected | User notifications |
| `advanced_search.html` | Advanced search | Public | Complex filters |
| `test_framework.html` | Testing page | Test | Testing utilities |

### 🔧 Cleanup Scripts Purpose

| Script | Function | Data Impact |
|--------|----------|-------------|
| `seed_data.py` | Generate test data | Populates all JSON files |
| `clear_data.py` | Remove all data | Clears all JSON files |
| `update_data.py` | Add more products | Adds to products.json |
| `fix_product_images.py` | Fix image URLs | Updates products.json |
| `cleanup_duplicate_likes.py` | Remove duplicates | Cleans likes.json |
| `test_like_validation.py` | Validate likes | Checks likes.json |
| `test_helpful_validation.py` | Validate helpful votes | Checks helpful_votes.json |

## 🌐 Web Interface Routes

```
GET    /                       - Home page
GET    /web/login              - Login page
GET    /web/register           - Registration page
GET    /web/products           - Products listing page
GET    /web/products/<id>      - Product detail page
GET    /web/cart               - Shopping cart page
GET    /web/orders             - Orders page
GET    /web/profile            - User profile page
GET    /web/admin              - Admin dashboard (Admin only)
```

---

## 📡 API Endpoints Details

### 🔐 Authentication Endpoints

#### Register New User
```
POST /api/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "phone": "1234567890",
  "address": "123 Main St"
}
```
**Response (201):** User created with ID, email, name, and timestamp

#### Login User
```
POST /api/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```
**Response (200):** Returns JWT token and user info

---

### 👥 User Management Endpoints

#### Get All Users (Admin Only)
```
GET /api/users
Authorization: Bearer {{admin_token}}
```
**Response (200):** Array of all users with pagination

#### Get User Profile
```
GET /api/users/{{user_id}}
Authorization: Bearer {{token}}
```
**Response (200):** Specific user details

#### Update User Profile
```
PUT /api/users/{{user_id}}
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "name": "John Updated",
  "phone": "9876543210",
  "address": "456 Oak Ave"
}
```
**Response (200):** Updated user information

#### Delete User (Admin Only)
```
DELETE /api/users/{{user_id}}
Authorization: Bearer {{admin_token}}
```
**Response (200):** User deletion confirmation

---

### 🛍️ Product Management Endpoints

#### Get All Products
```
GET /api/products?page=1&per_page=10&category=Electronics&min_price=10&max_price=1000
```
**Response (200):** Paginated product list with filters

#### Get Product by ID
```
GET /api/products/{{product_id}}
```
**Response (200):** Detailed product information

#### Create Product (Admin Only)
```
POST /api/products
Authorization: Bearer {{admin_token}}
Content-Type: application/json

{
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse",
  "price": 29.99,
  "category": "Electronics",
  "stock": 100,
  "image_url": "https://example.com/mouse.jpg"
}
```
**Response (201):** Created product with ID and timestamp

#### Update Product (Admin Only)
```
PUT /api/products/{{product_id}}
Authorization: Bearer {{admin_token}}
Content-Type: application/json

{
  "price": 24.99,
  "stock": 80
}
```
**Response (200):** Updated product details

#### Delete Product (Admin Only)
```
DELETE /api/products/{{product_id}}
Authorization: Bearer {{admin_token}}
```
**Response (200):** Product deletion confirmation

#### Search Products
```
GET /api/products/search?q=laptop
```
**Response (200):** Array of matching products

#### Get Products by Category
```
GET /api/products/category/{{category_name}}
```
**Response (200):** Products in specified category

---

### 🛒 Cart Management Endpoints

#### Get User Cart
```
GET /api/cart
Authorization: Bearer {{token}}
```
**Response (200):** Cart items with totals

#### Add Item to Cart
```
POST /api/cart/items
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```
**Response (201):** Item added confirmation

#### Update Cart Item
```
PUT /api/cart/items/{{item_id}}
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "quantity": 3
}
```
**Response (200):** Updated cart item

#### Remove Item from Cart
```
DELETE /api/cart/items/{{item_id}}
Authorization: Bearer {{token}}
```
**Response (200):** Item removal confirmation

#### Clear Entire Cart
```
DELETE /api/cart
Authorization: Bearer {{token}}
```
**Response (200):** Cart cleared confirmation

---

### 📦 Order Management Endpoints

#### Create Order
```
POST /api/orders
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "shipping_address": "123 Main St, City, State 12345"
}
```
**Response (201):** Order created with items and total

#### Get User Orders
```
GET /api/orders
Authorization: Bearer {{token}}
```
**Response (200):** All orders for authenticated user

#### Get Order by ID
```
GET /api/orders/{{order_id}}
Authorization: Bearer {{token}}
```
**Response (200):** Specific order details

#### Update Order (Shipping Address)
```
PUT /api/orders/{{order_id}}
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "shipping_address": "456 Oak Ave, City, State 67890"
}
```
**Response (200):** Updated order information

#### Update Order Status (Admin Only)
```
PUT /api/orders/{{order_id}}/status
Authorization: Bearer {{admin_token}}
Content-Type: application/json

{
  "status": "processing"
}
```
**Valid statuses:** pending, processing, shipped, delivered, cancelled

#### Cancel Order
```
DELETE /api/orders/{{order_id}}
Authorization: Bearer {{token}}
```
**Response (200):** Order cancellation confirmation

#### Get Orders by Status
```
GET /api/orders/status/{{status}}
Authorization: Bearer {{token}}
```
**Response (200):** Orders filtered by status

---

### ⭐ Reviews & Ratings Endpoints

#### Create Review
```
POST /api/reviews
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "product_id": 1,
  "rating": 5,
  "comment": "Excellent product, highly recommended!"
}
```
**Response (201):** Review created with ID and timestamp

#### Get Product Reviews
```
GET /api/products/{{product_id}}/reviews
```
**Response (200):** All reviews for product with average rating

#### Check if User Reviewed Product
```
GET /api/products/{{product_id}}/reviews/check
Authorization: Bearer {{token}}
```
**Response (200):** User's review status and details

---

### ❤️ Product Likes Endpoints

#### Like Product
```
POST /api/products/likes
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "product_id": 1
}
```
**Response (201):** Like created with timestamp

#### Get Product Likes Count
```
GET /api/products/{{product_id}}/likes
```
**Response (200):** Array of likes with count

#### Check User Like
```
GET /api/products/{{product_id}}/likes/check
Authorization: Bearer {{token}}
```
**Response (200):** User's like status

---

### 📚 Category Endpoints

#### Get All Categories
```
GET /api/categories
```
**Response (200):** Array of all categories

#### Create Category (Admin Only)
```
POST /api/categories
Authorization: Bearer {{admin_token}}
Content-Type: application/json

{
  "name": "Gaming",
  "description": "Gaming equipment and accessories"
}
```
**Response (201):** Category created

#### Delete Category (Admin Only)
```
DELETE /api/categories/{{category_id}}
Authorization: Bearer {{admin_token}}
```
**Response (200):** Category deletion confirmation

---

### 📊 Admin & Statistics Endpoints

#### Get Dashboard Statistics
```
GET /api/stats
Authorization: Bearer {{admin_token}}
```
**Response (200):** Total users, products, orders, revenue, pending orders, etc.

#### Get Low Stock Products
```
GET /api/inventory/low-stock?threshold=10
Authorization: Bearer {{admin_token}}
```
**Response (200):** Products below stock threshold

#### Update Product Stock
```
PUT /api/inventory/update-stock
Authorization: Bearer {{admin_token}}
Content-Type: application/json

{
  "product_id": 1,
  "stock": 100
}
```
**Response (200):** Stock update confirmation

#### Get User Activity (Admin Only)
```
GET /api/users/{{user_id}}/activity
Authorization: Bearer {{admin_token}}
```
**Response (200):** User activity summary with orders and reviews

#### Bulk Update Products (Admin Only)
```
PUT /api/products/bulk-update
Authorization: Bearer {{admin_token}}
Content-Type: application/json

{
  "updates": [
    {"product_id": 1, "price": 899.99, "stock": 75},
    {"product_id": 2, "price": 24.99, "stock": 200}
  ]
}
```
**Response (200):** Bulk update confirmation

#### Export Products
```
GET /api/export/products
Authorization: Bearer {{admin_token}}
```
**Response (200):** Products export with metadata

#### Export Orders
```
GET /api/export/orders?start_date=2024-11-01&end_date=2024-11-30
Authorization: Bearer {{admin_token}}
```
**Response (200):** Orders export for date range

---

### 📋 Help & Support Endpoints

#### Get Help Articles
```
GET /api/help?category=billing&page=1&per_page=10
```
**Response (200):** Paginated help articles by category

#### Get Help Categories
```
GET /api/help/categories
```
**Response (200):** Array of available help categories

#### Create Help Article (Admin Only)
```
POST /api/help
Authorization: Bearer {{admin_token}}
Content-Type: application/json

{
  "title": "How to track order?",
  "content": "You can track your order in the orders page...",
  "category": "shipping"
}
```
**Response (201):** Help article created

---

### 💬 Contact System Endpoints

#### Submit Contact Message
```
POST /api/contact
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Question about product",
  "message": "I have a question regarding..."
}
```
**Response (201):** Message received confirmation

#### Get Contact Messages (Admin Only)
```
GET /api/contact/messages
Authorization: Bearer {{admin_token}}
```
**Response (200):** All contact messages

---

### 🎁 Wishlist Endpoints

#### Get Wishlist
```
GET /api/wishlist
Authorization: Bearer {{token}}
```
**Response (200):** User's wishlist items with product details

#### Add to Wishlist
```
POST /api/wishlist
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "product_id": 1
}
```
**Response (201):** Item added to wishlist

#### Remove from Wishlist
```
DELETE /api/wishlist/{{item_id}}
Authorization: Bearer {{token}}
```
**Response (200):** Item removed from wishlist

---

### 🌐 System Monitoring Endpoints

#### Health Check
```
GET /api/health
```
**Response (200):** API status and timestamp

#### System Health Status
```
GET /api/system/health
```
**Response (200):** Comprehensive system status, data files, metrics

#### API Documentation
```
GET /api/docs
```
**Response (200):** Full API documentation with all endpoints

## 🧪 Testing Scenarios

### Manual Testing Workflows

#### Workflow 1: User Registration & Shopping
1. Register new account via `/web/register`
2. Login with credentials
3. Browse products on `/web/products`
4. View product details
5. Add products to cart
6. Proceed to checkout
7. Create order with shipping address
8. View order history on `/web/orders`
9. Leave product reviews and likes

#### Workflow 2: Admin Operations
1. Login as admin (`admin@test.com` / `admin123`)
2. Access admin dashboard `/web/admin`
3. Add/edit/delete products
4. View all orders and update status
5. Monitor inventory and low-stock alerts
6. View statistics and analytics
7. Manage users
8. Create help articles

#### Workflow 3: Product Management & Discovery
1. Filter products by category
2. Search for specific products
3. Sort by price and rating
4. View product reviews and ratings
5. Like/unlike products
6. Add items to wishlist
7. Compare product specifications
8. Check product availability

#### Workflow 4: Order & Payment Testing
1. Add multiple items to cart
2. Update quantities
3. Remove items from cart
4. Clear entire cart
5. Create order with different shipping addresses
6. View order status progression
7. Cancel order if needed
8. Track order history

### API Testing with Postman

#### Step 1: Import Collection
1. Open **Postman**
2. Click **Collections** → **Import**
3. Select `E-Commerce_API.postman_collection.json`
4. Collection appears in left sidebar organized by feature

#### Step 2: Create Environment
1. Click **Environments** → **Create New**
2. Name: `E-Commerce Dev`
3. Add variables:
```json
{
  "base_url": "http://localhost:5000/api",
  "web_url": "http://localhost:5000",
  "token": "",
  "admin_token": "",
  "user_id": "1",
  "product_id": "1",
  "order_id": "1"
}
```
4. Save and select as active environment

#### Step 3: Get Authentication Tokens
1. Register or login via the **Authentication** folder
2. Copy the `token` from response
3. Set it in Postman environment: **Environments** → Select environment → Set `token` value
4. For admin operations, get `admin_token` with admin credentials

#### Step 4: Test Endpoints
- Browse folders organized by feature (Products, Cart, Orders, etc.)
- Each request has pre-configured headers and body examples
- Use environment variables ({{variable_name}}) in requests
- Responses show expected data structure and status codes

#### Step 5: Automate with Newman (CLI)
```bash
newman run E-Commerce_API.postman_collection.json -e environment.json
```

**Example: Login Request**
```
POST {{base_url}}/login
Content-Type: application/json

{
  "email": "admin@test.com",
  "password": "admin123"
}
```

**Example: Get Products**
```
GET {{base_url}}/products?page=1&per_page=10&category=Electronics
```

**Example: Add to Cart**
```
POST {{base_url}}/cart/items
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

### Automation Testing (Selenium)

All HTML elements have unique IDs for Selenium automation:

**Login Elements:**
```python
email_field = driver.find_element(By.ID, "login-email")
password_field = driver.find_element(By.ID, "login-password")
login_button = driver.find_element(By.ID, "btn-login-submit")
```

**Product Elements:**
```python
product_card = driver.find_element(By.ID, "product-1")
add_to_cart_btn = driver.find_element(By.ID, "btn-add-cart-1")
product_name = driver.find_element(By.ID, "product-name-1")
```

**Cart Elements:**
```python
cart_item = driver.find_element(By.ID, "cart-item-1")
increase_qty = driver.find_element(By.ID, "btn-increase-1")
checkout_btn = driver.find_element(By.ID, "btn-checkout")
```

**Admin Elements:**
```python
products_table = driver.find_element(By.ID, "admin-products-table")
edit_product_btn = driver.find_element(By.ID, "btn-edit-product-1")
stats_panel = driver.find_element(By.ID, "dashboard-stats")
```

### Sample Test Scenarios

**Scenario 1: Complete Purchase Journey**
1. Register with new email
2. Search for "Laptop"
3. Add product to cart
4. View cart and verify totals
5. Update quantity
6. Proceed to checkout
7. Verify order confirmation
8. Leave review (5 stars)
9. Like the product

**Scenario 2: Admin Inventory Management**
1. Login as admin
2. Create new product category
3. Add 3 new products
4. Update prices on 2 products
5. Check low-stock alerts
6. Export inventory report
7. Bulk update stock levels

**Scenario 3: Error Handling**
1. Try to register with existing email → Expect 409 Conflict
2. Login with wrong password → Expect 401 Unauthorized
3. Access admin endpoint as user → Expect 403 Forbidden
4. Request non-existent product → Expect 404 Not Found
5. Submit empty form → Expect 400 Bad Request

## 📊 Database Management

### View Data
```
# Check users
cat data/users.json

# Check products
cat data/products.json

# Check orders
cat data/orders.json
```

### Clear All Data
```
python clear_data.py
```

### Add More Products
```
python update_data.py
```

### Manual Data Modification
You can directly edit JSON files in the `data/` directory:
- `data/users.json` - User accounts
- `data/products.json` - Products
- `data/orders.json` - Orders
- `data/cart.json` - Cart items
- `data/categories.json` - Categories
- `data/reviews.json` - Reviews

## 🔧 Configuration

Edit `config.py` to customize:

```
SECRET_KEY = 'your-secret-key'           # Change in production
JWT_SECRET_KEY = 'your-jwt-secret'       # Change in production
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Token expiration
```

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **401 Unauthorized** | Token missing or expired. Re-login and update `{{token}}` in Postman environment |
| **403 Forbidden** | Not an admin. Use `{{admin_token}}` for admin endpoints |
| **404 Not Found** | Resource doesn't exist. Verify ID in URL parameters |
| **400 Bad Request** | Missing required fields in request body. Check endpoint documentation |
| **409 Conflict** | User already exists. Use different email for registration |
| **500 Internal Server Error** | Server error. Check Flask console for error details. Restart server if needed |

### Port Already in Use
```cmd
# Change port in app.py (last line)
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Data Not Loading
```bash
# Regenerate test data
python clear_data.py
python seed_data.py
```

### CORS Issues
CORS is enabled by default. If you still face issues, verify `app.py` contains:
```python
CORS(app)  # This should be present at the top
```

### Token Expiration
- Default token expiration: 24 hours
- If token expires during testing, re-login to get new token
- Update `{{token}}` variable in Postman environment

### Data Files Not Found
```bash
# Check data directory exists
ls data/

# If missing, run seed_data
python seed_data.py
```

### Template Not Found Error
Ensure `templates/` directory exists with all HTML files:
```bash
ls templates/
```

### API Returns Empty Response
1. Check if data files in `data/` directory are populated
2. Verify JSON syntax in data files (use online JSON validator)
3. Regenerate data: `python clear_data.py && python seed_data.py`

## 📝 API Response Format

### Standard Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Standard Error Response
```json
{
  "success": false,
  "error": "Detailed error message description"
}
```

### Paginated Response
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 75,
    "pages": 8
  }
}
```

### List Response with Count
```json
{
  "success": true,
  "data": [...],
  "count": 45
}
```

---

## ✅ Postman Testing Workflows

### Workflow 1: Complete User Registration & Purchase

1. **Register New User**
   - `POST /api/register` with unique email
   - Save user ID from response

2. **Login**
   - `POST /api/login` with registered credentials
   - Copy `token` to environment variable

3. **Browse Products**
   - `GET /api/products?page=1&per_page=10`
   - Note product ID for next step

4. **Add to Cart**
   - `POST /api/cart/items` with product_id and quantity
   - Save cart item ID

5. **View Cart**
   - `GET /api/cart` to verify items and total

6. **Create Order**
   - `POST /api/orders` with shipping address
   - Verify cart is cleared after order

7. **Get Order Details**
   - `GET /api/orders/{{order_id}}` to confirm order

### Workflow 2: Admin Operations & Inventory

1. **Login as Admin**
   - `POST /api/login` with admin@test.com / admin123
   - Save `admin_token` to environment

2. **Create New Product**
   - `POST /api/products` with product details
   - Admin only endpoint

3. **View Statistics**
   - `GET /api/stats` to see dashboard data

4. **Check Low Stock**
   - `GET /api/inventory/low-stock?threshold=10`

5. **Update Stock**
   - `PUT /api/inventory/update-stock` with product and new stock level

6. **Bulk Update Products**
   - `PUT /api/products/bulk-update` with multiple products

7. **Export Orders**
   - `GET /api/export/orders?start_date=2024-11-01&end_date=2024-11-30`

8. **View User Activity**
   - `GET /api/users/{{user_id}}/activity` for user analytics

### Workflow 3: Product Engagement & Reviews

1. **Login User**
   - `POST /api/login` with regular user credentials
   - Save token

2. **Search Products**
   - `GET /api/products/search?q=laptop`

3. **Get Product Details**
   - `GET /api/products/{{product_id}}`

4. **Like Product**
   - `POST /api/products/likes` with product_id

5. **Check Like Status**
   - `GET /api/products/{{product_id}}/likes/check`

6. **Create Review**
   - `POST /api/reviews` with rating 1-5 and comment

7. **Get Product Reviews**
   - `GET /api/products/{{product_id}}/reviews` to see all reviews and average rating

8. **Check User Review**
   - `GET /api/products/{{product_id}}/reviews/check` to verify user has reviewed

### Workflow 4: Wishlist Management

1. **Get Wishlist**
   - `GET /api/wishlist` to view current items

2. **Add to Wishlist**
   - `POST /api/wishlist` with product_id

3. **Verify Item Added**
   - `GET /api/wishlist` to confirm

4. **Remove from Wishlist**
   - `DELETE /api/wishlist/{{item_id}}`

5. **Verify Removal**
   - `GET /api/wishlist` to confirm deletion

### Workflow 5: Customer Support

1. **Submit Contact Message**
   - `POST /api/contact` with name, email, subject, message

2. **Get Help Articles**
   - `GET /api/help?category=billing`

3. **View Help Categories**
   - `GET /api/help/categories`

4. **(Admin) View Contact Messages**
   - `GET /api/contact/messages` with admin token

## 🎓 For Graduation Projects

This project is ideal for:

1. **Software Testing Projects**
   - Functional testing
   - API testing
   - Automation testing
   - Integration testing
   - Performance testing

2. **Test Documentation**
   - Test cases for all features
   - API testing documentation
   - Bug reports and tracking
   - Test automation scripts

3. **Tools Integration**
   - Postman collections
   - Selenium test scripts
   - JMeter load tests
   - pytest test suites

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [REST API Best Practices](https://restfulapi.net/)
- [JWT Authentication](https://jwt.io/)
- [Selenium WebDriver](https://www.selenium.dev/documentation/)
- [Postman API Testing](https://learning.postman.com/)

## 🤝 Contributing

This is a learning project. Feel free to:
- Add more features
- Improve the UI
- Add more test scenarios
- Create test automation scripts
- Enhance security features

## ⚠️ Important Notes

### Security
- This is a **learning/testing project**
- NOT production-ready
- Passwords are hashed with SHA256 (use bcrypt in production)
- Change SECRET_KEY and JWT_SECRET_KEY in production
- Add rate limiting for production use
- Implement proper input validation

### Data Persistence
- JSON files are simple and easy to understand
- Data persists between server restarts
- No database server required
- Perfect for testing and learning

### Performance
- Suitable for testing and development
- For production, use a real database (PostgreSQL, MySQL)
- Current implementation loads entire files into memory

## 📄 License

MIT License - Free to use for learning and testing purposes.

## 👤 Author

Created for software testing education and API testing practice.

## 🎯 Next Steps

1. ✅ Generate test data with `python seed_data.py`
2. ✅ Start the server with `python app.py`
3. ✅ Open browser to `http://localhost:5000`
4. ✅ Login with test credentials
5. ✅ Explore the API and UI
6. ✅ Start testing!

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review the API documentation
- Inspect JSON files in `data/` directory
- Check browser console for errors
- Verify all dependencies are installed

---

**Happy Testing! 🚀**

Built with ❤️ for Software Testers and QA Engineers
```

Now your project has complete documentation! Save this as `README.md` in your project root directory. It includes:

✅ Complete project overview
✅ All API endpoints documented
✅ Installation instructions
✅ Test credentials
✅ Project structure
✅ Testing scenarios
✅ Selenium element IDs guide
✅ Troubleshooting tips
✅ Database management
✅ Configuration options
✅ Security notes
✅ Learning resources

