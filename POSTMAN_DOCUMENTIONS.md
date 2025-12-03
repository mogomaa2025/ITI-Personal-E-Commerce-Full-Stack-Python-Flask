# Postman Collection Guide - E-Commerce API

Complete guide to importing and using the E-Commerce API with Postman, including all endpoints, request bodies, and expected responses.

---

## 🔐 Authentication

### 🆕 Important: v2.2 Changes
**Login now returns TWO tokens:**
- `token` - Access token (24 hours) - Use for all API requests
- `refresh_token` - Refresh token (30 days) - Use to get new access tokens

**Update your Postman environment with:**
```json
{
  "token": "",
  "refresh_token": ""
}
```

---

### Register New User

**Endpoint:** `POST /api/register`

**Request:**
```json
{
    "email": "{{email}}",
    "password": "Gomaa@123",
    "name": "test",
    "is_admin": false
}
```

**Response (201):**
```json
{
    "data": {
        "address": "",
        "created_at": "2025-11-13T13:53:09.096764",
        "email": "test_iubwwii4@gmail.com",
        "id": 115,
        "is_admin": false,
        "name": "test",
        "phone": ""
    },
    "message": "User registered successfully",
    "success": true
}
```

**Response (400): empty fields**
```json
{
    "error": "Email and password are required",
    "success": false
}    
```
**Response (400): invalid field**
```json
{
    "error": "Invalid email format",
    "success": false
}    
```

**Response (409): user already exists**
```json
{
    "error": "User already exists",
    "success": false
}    
```



---

### Login User

**Endpoint:** `POST /api/login`

**Request:**
```json
{
    "email": "{{email}}",
    "password": "Gomaa@123"
}
```

**Response (200):**
```json
{
    "message": "Login successful",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.jwt2 .jwt3",
    "success": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.jwt2.jwt3",
    "user": {
        "email": "test_iubwwii4@gmail.com",
        "id": 115,
        "is_admin": false,
        "name": "test"
    }
}
```
**Response (401): invalid credentials**
```json
{
    "error": "Invalid credentials",
    "success": false
}
```
**Response (400): missing credentials**
```json
{
    "error": "Email and password are required",
    "success": false
}
```




**⚠️ IMPORTANT:** Copy BOTH tokens and set them in Postman automatic using testscript or manually

### Login Admin

**Endpoint:** `POST /api/login`

**Request:**
```json
{
    "email": "admin@test.com",
    "password": "admin123"
}
```


**Response now includes:**
```json
{
    "message": "Login successful",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.jwt2.jwt3", // Refresh token (30d)
    "success": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.jwt2.jwt3",  // Access token (24h)
    "user": {
        "email": "admin@test.com",
        "id": 40,
        "is_admin": true,
        "name": "admin"
    }
}
```

---

## 🆕 New in v2.2: Token Refresh Endpoint

### Refresh Access Token

**Endpoint:** `POST /api/refresh`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
    "refresh_token": "{{refresh_admin_token}}"
}
```

**Response (200):**
```json
{
    "message": "Token refreshed successfully",
    "success": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.jwt2.jwt3"
}
```

**Error Responses:**
- 400: Missing refresh token
- 401: Invalid or expired refresh token
- 401: Wrong token type (used access token instead of refresh)
- 404: User not found

**When to use:**
- Access token expires after 24 hours
- Instead of logging in again, use refresh token to get new access token
- Refresh token valid for 30 days

---


## 📡 API Endpoints with Examples

### ✅ Health Check

**Endpoint:** `GET /api/health`

**Headers:**
```
Content-Type: application/json
```

**Response (200):**
```json
{
    "message": "API is running",
    "success": true,
    "timestamp": "2025-11-13T15:19:15.073597"
}
```

---

## 🌐 System Monitoring

### System Health Status

**Endpoint:** `GET /api/system/health`

**Response (200):**
```json
{
    "data_files": {
        "analytics.json": "ok",
        "cart.json": "ok",
        "categories.json": "ok",
        "contact_messages.json": "ok",
        "coupons.json": "ok",
        "help.json": "ok",
        "notifications.json": "ok",
        "orders.json": "ok",
        "products.json": "ok",
        "reviews.json": "ok",
        "users.json": "ok",
        "wishlist.json": "ok"
    },
    "metrics": {
        "total_orders": 100,
        "total_products": 80,
        "total_users": 116
    },
    "status": "healthy",
    "success": true,
    "timestamp": "2025-11-13T15:21:25.495913"
}
```

---

### API Documentation

**Endpoint:** `GET /api/docs`

**Response (200):**
```json
{
    "base_url": "http://127.0.0.1:5000/api",
    "description": "Comprehensive e-commerce API with advanced features",
    "endpoints": {
        "admin": {
            "GET /api/export/orders": "Export orders",
            "GET /api/export/products": "Export products",
            "GET /api/inventory/low-stock": "Get low stock products",
            "GET /api/stats": "Get dashboard statistics",
            "GET /api/users/{id}/activity": "Get user activity",
            "PUT /api/inventory/update-stock": "Update product stock",
            "PUT /api/products/bulk-update": "Bulk update products"
        },
        "analytics": {
            "GET /api/analytics/dashboard": "Get dashboard analytics (Admin)",
            "GET /api/analytics/reports/sales": "Get sales report (Admin)"
        },
        "authentication": {
            "POST /api/login": "User login",
            "POST /api/register": "Register a new user"
        },
        "blog": {
            "GET /api/blog/posts": "Get blog posts",
            "GET /api/blog/posts/{id}": "Get blog post"
        },
        "cart": {
            "DELETE /api/cart": "Clear cart",
            "DELETE /api/cart/items/{id}": "Remove from cart",
            "GET /api/cart": "Get user cart",
            "POST /api/cart/items": "Add item to cart",
            "PUT /api/cart/items/{id}": "Update cart item"
        },
        "contact": {
            "GET /api/contact/messages": "Get contact messages (Admin)",
            "POST /api/contact": "Submit contact message",
            "POST /api/contact/messages/{id}/respond": "Respond to message (Admin)"
        },
        "coupons": {
            "GET /api/coupons": "Get available coupons",
            "POST /api/coupons": "Create coupon (Admin)",
            "POST /api/coupons/validate": "Validate coupon code"
        },
        "help": {
            "GET /api/help": "Get help articles",
            "GET /api/help/categories": "Get help categories",
            "GET /api/help/{id}": "Get help article",
            "POST /api/help": "Create help article (Admin)",
            "POST /api/help/{id}/helpful": "Mark article helpful",
            "PUT /api/help/{id}": "Update help article (Admin)"
        },
        "notifications": {
            "GET /api/notifications": "Get user notifications",
            "PUT /api/notifications/read-all": "Mark all notifications as read",
            "PUT /api/notifications/{id}/read": "Mark notification as read"
        },
        "orders": {
            "DELETE /api/orders/{id}": "Cancel order",
            "GET /api/orders": "Get user orders",
            "GET /api/orders/status/{status}": "Get orders by status",
            "GET /api/orders/{id}": "Get order by ID",
            "POST /api/orders": "Create order",
            "PUT /api/orders/{id}": "Update order details (shipping address)",
            "PUT /api/orders/{id}/status": "Update order status (Admin)"
        },
        "products": {
            "DELETE /api/products/{id}": "Delete product (Admin)",
            "GET /api/products": "Get all products with filtering",
            "GET /api/products/category/{category}": "Get products by category",
            "GET /api/products/search": "Search products",
            "GET /api/products/{id}": "Get product by ID",
            "POST /api/products": "Create product (Admin)",
            "PUT /api/products/{id}": "Update product (Admin)"
        },
        "recommendations": {
            "GET /api/recommendations/user/{id}": "Get user recommendations",
            "GET /api/recommendations/{id}": "Get product recommendations"
        },
        "reviews": {
            "GET /api/products/{id}/reviews": "Get product reviews",
            "POST /api/reviews": "Create product review"
        },
        "search": {
            "GET /api/search/advanced": "Advanced product search"
        },
        "system": {
            "GET /api/docs": "API documentation",
            "GET /api/health": "Health check",
            "GET /api/system/health": "System health status"
        },
        "users": {
            "DELETE /api/users/{id}": "Delete user (Admin)",
            "GET /api/users": "Get all users (Admin)",
            "GET /api/users/{id}": "Get user by ID",
            "PUT /api/users/{id}": "Update user information"
        },
        "wishlist": {
            "DELETE /api/wishlist/{id}": "Remove from wishlist",
            "GET /api/wishlist": "Get user wishlist",
            "POST /api/wishlist": "Add to wishlist"
        }
    },
    "features": [
        "User Authentication & Management",
        "Product Catalog & Inventory",
        "Shopping Cart & Orders",
        "Reviews & Ratings",
        "Help & FAQ System",
        "Contact Management",
        "Wishlist Functionality",
        "Coupon & Discount System",
        "Notification System",
        "Analytics & Reporting",
        "Advanced Search",
        "Product Recommendations",
        "Blog & Content Management",
        "Admin Dashboard",
        "Bulk Operations",
        "Data Export",
        "System Monitoring"
    ],
    "success": true,
    "title": "E-Commerce API Documentation",
    "total_endpoints": 62,
    "version": "2.0"
}
```
---


## 👥 User Management

### Get All Users (Admin Only)

**Endpoint:** `GET /api/users`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "count": 116,
    "data": [
        {
            "address": "226 Oak Ave, Indianapolis, CA 90001",
            "created_at": "2025-02-14T00:17:15.199498",
            "email": "user@test.com",
            "id": 2,
            "is_admin": false,
            "name": "Test User",
            "phone": "555-0101"
        }
        ],
    "success": true
}
```

**Response (403): forbidden no admin token** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```
**Response (401): UNAUTHORIZED no token** new
```json
{
    "error": "Token is missing",
    "success": false
}
```


---

### Get User Profile

**Endpoint:** `GET /api/users/{{user_id}}`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "address": "",
        "created_at": "2025-11-13T14:48:43.634900",
        "email": "test_q9wh3p5s@gmail.com",
        "id": 120,
        "is_admin": false,
        "name": "test",
        "phone": ""
    },
    "success": true
}
```
**Response (404): id user not found** new
```json
{
    "error": "User not found",
    "success": false
}
```


---

### Update User Profile

**Endpoint:** `PUT /api/users/{{user_id}}`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "name": "todelete2",
    "phone": "555-0101",
    "address": "123 Updated Street"
}
```

**Response (200):**
```json
{
    "data": {
        "address": "123 Updated Street",
        "created_at": "2025-11-13T14:48:43.634900",
        "email": "test_q9wh3p5s@gmail.com",
        "id": 120,
        "is_admin": false,
        "name": "todelete2",
        "phone": "555-0101",
        "updated_at": "2025-11-13T15:24:53.356610"
    },
    "message": "User updated successfully",
    "success": true
}
```
**Response (404): id user not found** new
```json
{
    "error": "User not found",
    "success": false
}
```


---

### Delete User (Admin Only)

**Endpoint:** `DELETE /api/users/{{user_id}}`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "email": "test_q9wh3p5s@gmail.com",
        "id": 120
    },
    "message": "User deleted successfully",
    "success": true
}
```
**Response (404) when no user id found:**
```json
{
    "error": "User not found",
    "success": false
}
```
**Response (403) Forbidden when user_token instead admin_token:** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```
**Response (401) UNAUTHORIZED when no token:** new
```json
{
    "error": "Token is missing",
    "success": false
}
```

---

### Get User Activity (Admin Only)

**Endpoint:** `GET /api/users/10/activity`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Response (200):**
{
    "data": {
        "cart_items": 0,
        "orders": [],
        "reviews": [],
        "total_orders": 0,
        "total_reviews": 0,
        "total_spent": 0,
        "user_id": 120
    },
    "success": true
}

**Response (403) Forbidden when user_token instead admin_token:** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```
**Response (401) UNAUTHORIZED when no token:** new
```json
{
    "error": "Token is missing",
    "success": false
}
```

---


## 📚 Categories 


### Create Category (Admin Only)

**Endpoint:** `POST /api/categories`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "name": "TestCategory",
    "description": "Test Category"
}
```

**Response (201):**
```json
{
    "data": {
        "created_at": "2025-11-13T16:15:36.599127",
        "description": "Test Category",
        "id": 9,
        "name": "TestCategory"
    },
    "message": "Category created successfully",
    "success": true
}
```
**Response (403) Forbidden when user_token instead admin_token:** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```
---


### Get All Categories

**Endpoint:** `GET /api/categories`

**Response (200):**
```json
{
    "count": 9,
    "data": [
        {
            "created_at": "2024-12-06T00:17:15.200501",
            "description": "Electronic devices and accessories",
            "id": 1,
            "name": "Electronics"
        },
        {
            "created_at": "2024-12-01T00:17:15.200501",
            "description": "Fashion and apparel",
            "id": 2,
            "name": "Clothing"
        },
        {
            "created_at": "2024-10-24T00:17:15.200501",
            "description": "Books and publications",
            "id": 3,
            "name": "Books"
        },
        {
            "created_at": "2024-10-20T00:17:15.200501",
            "description": "Home improvement and garden supplies",
            "id": 4,
            "name": "Home & Garden"
        },
        {
            "created_at": "2025-10-16T02:09:30.902195",
            "description": "Accessory items",
            "id": 5,
            "name": "Accessories"
        },
        {
            "created_at": "2025-10-17T14:41:31.012279",
            "description": "Accessory items",
            "id": 6,
            "name": "Accessories"
        },
        {
            "created_at": "2025-11-12T22:48:08.661937",
            "description": "Accessory items",
            "id": 7,
            "name": "Accessories"
        },
        {
            "created_at": "2025-11-13T16:12:51.886959",
            "description": "Accessory items",
            "id": 8,
            "name": "Accessories"
        },
        {
            "created_at": "2025-11-13T16:15:36.599127",
            "description": "Test Category",
            "id": 9,
            "name": "TestCategory"
        }
    ],
    "success": true
}
```

---

### Delete Category (Admin Only)

**Endpoint:** `DELETE /api/categories/{{category_id}}`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "id": 9,
        "name": "TestCategory"
    },
    "message": "Category deleted successfully",
    "success": true
}
```
**Response (404) when no category id found:** new
```json
{
    "error": "Category not found",
    "success": false
}
```
**Response (403) Forbidden when user_token instead admin_token:** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```
---

## 🛍️ Product Management


'' **Get All Products** ''


**Endpoint:** `GET /api/products`
**Response (200):**
```json
{
  "success": true,
   "data": [
        {
            "category": "Electronics",
            "created_at": "2025-09-15T00:17:15.200501",
            "description": "High-performance laptop with 16GB RAM and 512GB SSD2",
            "id": 1,
            "image_url": "https://picsum.photos/400/300?random=1",
            "name": "Laptop Pro 15\"",
            "price": 1299.99,
            "stock": 51,
            "updated_at": "2025-10-14T21:22:50.472349"
        }
  ],
  "pagination": {
     "page": 1,
        "pages": 9,
        "per_page": 10,
        "total": 82
  }
}
```
---


 **Query Products [new]** 


**Endpoint:** `GET /api/products`
**Query Filter Products [new]**
```
page=1
per_page=10
category=Electronics
min_price=10
max_price=1000
search=
```

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Laptop Pro",
      "description": "High-performance laptop",
      "price": 999.99,
      "category": "Electronics",
      "stock": 50,
      "image_url": "https://example.com/laptop.jpg",
      "created_at": "2024-11-12T10:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 50,
    "pages": 5
  }
}
```

---

### Create Product (Admin Only)

**Endpoint:** `POST /api/products`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "name": "new product1",
    "description": "new product description1",
    "price": 29.99,
    "category": "Electronics",
    "stock": 20,
    "image_url": "https://ci.suez.edu.eg/wp-content/uploads/2022/08/iti-logo.png"
}
```

**Response (201):**
```json
{
    "data": {
        "category": "Electronics",
        "created_at": "2025-11-13T15:53:14.533983",
        "description": "new product description1",
        "id": 83,
        "image_url": "https://ci.suez.edu.eg/wp-content/uploads/2022/08/iti-logo.png",
        "name": "new product1",
        "price": 29.99,
        "stock": 20
    },
    "message": "Product created successfully",
    "success": true
}
```


**Request:**
```json
{
    "name": "test"
}
```

**Response (400)bad request: if no product detials** new
```json
{
    "error": "Missing required fields",
    "success": false
}
```



**Response (403)forbidden: if user_token instead of admin_token** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```



---

### Update Product (Admin Only)

**Endpoint:** `PUT /api/products/{{product_id}}`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "description": "Updated description",
    "price": 34.99,
    "stock": 75
}
```

**Response (200):**
```json
{
    "data": {
        "category": "Electronics",
        "created_at": "2025-11-13T15:53:14.533983",
        "description": "Updated description",
        "id": 83,
        "image_url": "https://ci.suez.edu.eg/wp-content/uploads/2022/08/iti-logo.png",
        "name": "new product1",
        "price": 34.99,
        "stock": 75,
        "updated_at": "2025-11-13T15:54:39.776502"
    },
    "message": "Product updated successfully",
    "success": true
}
```
**Response (404):non existing product** new
```json
{
    "error": "Product not found",
    "success": false
}
```
---

### Get Product by ID

**Endpoint:** `GET /api/products/{{product_id}}`

**Response (200):**
```json
{
    "data": {
        "category": "Electronics",
        "created_at": "2025-11-13T15:53:14.533983",
        "description": "Updated description",
        "id": 83,
        "image_url": "https://ci.suez.edu.eg/wp-content/uploads/2022/08/iti-logo.png",
        "name": "new product1",
        "price": 34.99,
        "stock": 75,
        "updated_at": "2025-11-13T15:55:08.557699"
    },
    "success": true
}
```
**Response (404):**
```json
{
    "error": "Product not found",
    "success": false
}
```




---

### Delete Product (Admin Only)

**Endpoint:** `DELETE /api/products/{{product_id}}`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "id": 83,
        "name": "new product1"
    },
    "message": "Product deleted successfully",
    "success": true
}
```
**Response (404):**
```json
{
    "error": "Product not found",
    "success": false
}
```

---

### Search Products

**Endpoint:** `GET /api/products/search`

**Query Parameters:**
```
q=laptop
```

**Response (200):**
```json
{
    "count": 2,
    "data": [
        {
            "category": "Electronics",
            "created_at": "2025-09-15T00:17:15.200501",
            "description": "High-performance laptop with 16GB RAM and 512GB SSD2",
            "id": 1,
            "image_url": "https://picsum.photos/400/300?random=1",
            "name": "Laptop Pro 15\"",
            "price": 1299.99,
            "stock": 51,
            "updated_at": "2025-10-14T21:22:50.472349"
        },
        {
            "category": "Electronics",
            "created_at": "2025-09-30T00:17:15.200501",
            "description": "Adjustable aluminum laptop stand",
            "id": 15,
            "image_url": "https://picsum.photos/400/300?random=15",
            "name": "Laptop Stand",
            "price": 49.99,
            "stock": 21
        }
    ],
    "success": true
}
```
**Response (200): no matching data** new
```json
{
    "count": 0,
    "data": [],
    "success": true
}
```


---

### Get Products by Category

**Endpoint:** `GET /api/products/category/Electronics`

**Response (200):**
```json
{
    "count": 22,
    "data": [
        {
            "category": "Electronics",
            "created_at": "2025-09-15T00:17:15.200501",
            "description": "High-performance laptop with 16GB RAM and 512GB SSD2",
            "id": 1,
            "image_url": "https://picsum.photos/400/300?random=1",
            "name": "Laptop Pro 15\"",
            "price": 1299.99,
            "stock": 51,
            "updated_at": "2025-10-14T21:22:50.472349"
        },
        {
            "category": "Electronics",
            "created_at": "2025-07-12T00:17:15.200501",
            "description": "Ergonomic wireless mouse with precision tracking",
            "id": 2,
            "image_url": "https://picsum.photos/400/300?random=2",
            "name": "Wireless Mouse",
            "price": 29.99,
            "stock": 142
        },
        {
            "category": "Electronics",
            "created_at": "2025-08-11T00:17:15.200501",
            "description": "RGB mechanical keyboard with Cherry MX switches",
            "id": 3,
            "image_url": "https://picsum.photos/400/300?random=3",
            "name": "Mechanical Keyboard",
            "price": 149.99,
            "stock": 40
        }
    ],
    "success": true
}
```

**Endpoint:** `GET /api/products/category/NonExistent`

**Response (200):**
```json
{
    "count": 0,
    "data": [],
    "success": true
}
```

---

### Get Low Stock Products (Admin Only)

**Endpoint:** `GET /api/inventory/low-stock`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Query Parameters:**
```
threshold=10
```

**Response (200):**
```json
{
    "count": 1,
    "data": [
        {
            "category": "Books",
            "created_at": "2025-04-20T00:17:15.200501",
            "description": "Complete guide to Python programming",
            "id": 31,
            "image_url": "https://dummyimage.com/400x300/1abc9c/ffffff&text=Product",
            "name": "Python Programming Guide",
            "price": 39.99,
            "stock": 10
        }
    ],
    "success": true,
    "threshold": 10
}
```

**Query Parameters:**
```
threshold=5
```
**Response (200): low stock custom threshold** new
```json
{
    "count": 0,
    "data": [],
    "success": true,
    "threshold": 5
}
```


---

### Update Product Stock (Admin Only)

**Endpoint:** `PUT /api/inventory/update-stock`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "product_id": 4,
    "stock": 40
}
```

**Response (200):**
```json
{
    "data": {
        "new_stock": 40,
        "old_stock": 60,
        "product_id": 4
    },
    "message": "Stock updated successfully",
    "success": true
}
```

**Request: non existing product**
```json
{
    "product_id": 444444,
    "stock": 40
}
```

**Response (404): non existing product** new
```json
{
    "error": "Product not found",
    "success": false
}
```

---

### Bulk Update Products (Admin Only)

**Endpoint:** `PUT /api/products/bulk-update`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "updates": [
        {
            
            "product_id": 4,
            "price": 24.98,
            "stock": 60
        }
    ]
}
```


**Response (200):**
```json
{
    "message": "1 products updated successfully",
    "success": true,
    "updated_count": 1
}
```


**Request we can update more than one product:**
```json
{
  "updates": [
    {
      "product_id": 1,
      "price": 899.99,
      "stock": 75
    },
    {
      "product_id": 2,
      "price": 24.99,
      "stock": 200
    }
  ]
}
```
---

### Export Products (Admin Only)

**Endpoint:** `GET /api/export/products`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "export_date": "2025-11-13T16:54:11.798694",
        "products": [
            {
                "category": "Electronics",
                "created_at": "2025-09-15T00:17:15.200501",
                "description": "High-performance laptop with 16GB RAM and 512GB SSD2",
                "id": 1,
                "image_url": "https://picsum.photos/400/300?random=1",
                "name": "Laptop Pro 15\"",
                "price": 1299.99,
                "stock": 51,
                "updated_at": "2025-10-14T21:22:50.472349"
            },
            {
                "category": "Electronics",
                "created_at": "2025-07-12T00:17:15.200501",
                "description": "Ergonomic wireless mouse with precision tracking",
                "id": 2,
                "image_url": "https://picsum.photos/400/300?random=2",
                "name": "Wireless Mouse",
                "price": 24.98,
                "stock": 60,
                "updated_at": "2025-11-13T16:53:29.618847"
            }
            ],
        "total_products": 82
    },
    "success": true
}
```



---

## ❤️ Product Likes

### Like Product

**Endpoint:** `POST /api/products/likes`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Request:**
```json
{
  "product_id": 1
}
```

**Response (201):**
```json
{
    "data": {
        "created_at": "2025-11-13T14:58:57.302518",
        "id": 18,
        "product_id": 2,
        "user_id": 120
    },
    "message": "Product liked successfully",
    "success": true
}
```
**Response (400) Bad Request 2nd time:**
```json
{
    "already_liked": true,
    "error": "You have already liked this product",
    "success": false
}
```

 
**Request: in case invalid or non exist product** new
```json
{
  "product_id": 999999
}
```
**Response (400) Bad Request 2nd time:**
```json
{
      "error": "Product not found",
    "success": false
}
```
---

### Get Product Likes Count

**Endpoint:** `GET /api/products/{{product_id}}/likes`

**Response (200):**
```json
{
    "count": 6,
    "data": [
        {
            "created_at": "2025-10-19T22:26:04.626577",
            "id": 1,
            "product_id": 1,
            "user_id": 2
        },
        {
            "created_at": "2025-10-19T22:28:24.707825",
            "id": 2,
            "product_id": 1,
            "user_id": 64
        },
        {
            "created_at": "2025-10-21T23:53:04.463472",
            "id": 9,
            "product_id": 1,
            "user_id": 47
        },
        {
            "created_at": "2025-11-13T14:40:56.578021",
            "id": 12,
            "product_id": 1,
            "user_id": 40
        },
        {
            "created_at": "2025-11-13T14:41:23.063634",
            "id": 13,
            "product_id": 1,
            "user_id": 118
        },
        {
            "created_at": "2025-11-13T14:57:16.634411",
            "id": 17,
            "product_id": 1,
            "user_id": 120
        }
    ],
    "success": true
}
```

---

### Check User Like

**Endpoint:** `GET /api/products/{{product_id}}/likes/check`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "created_at": "2025-11-13T14:57:16.634411",
        "id": 17,
        "product_id": 1,
        "user_id": 120
    },
    "liked": true,
    "success": true
}
```

---

## 🆕 New in v2.2: Unlike Product Endpoint

### Unlike Product (Remove Like)

**Endpoint:** `DELETE /api/products/likes/{{like_id}}`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "created_at": "2025-11-13T14:57:16.634411",
        "id": 17,
        "product_id": 1,
        "user_id": 120
    },
    "message": "Product unliked successfully",
    "success": true
}
```
**Response (404) non found like id:**
```json
{
    "error": "Like not found",
    "success": false
}
```
**Response (403) FORBIDDEN: unlike another user's like**
```json
{
    "error": "Unauthorized",
    "success": false
}
```

**Error Responses:**
- 401: Not authenticated
- 403: Not your like
- 404: Like not found

---





## 🛒 Cart Management



### Clear Entire Cart

**Endpoint:** `DELETE /api/cart`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "message": "Cart cleared successfully",
    "success": true
}
```


---

### Add Item to Cart

**Endpoint:** `POST /api/cart/items`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "product_id": 4,
    "quantity": 2
}
```

**Response (201):**
```json
{
    "message": "Item added to cart successfully",
    "success": true
}
```
**Request:**
```json
{
    "product_id": 9999,
    "quantity": 1
}
```

**Response (404): if product not found** new
```json
{
    "error": "Product not found",
    "success": false
}
```
**Request:**
```json
{
    "product_id": 4,
    "quantity": 0
}
```

**Response (400) bad request: if product quantity invalid** new
```json
{
    "error": "Invalid quantity: must be a positive integer",
    "success": false
}
```
---


### Get User Cart

**Endpoint:** `GET /api/cart`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "count": 1,
    "data": [
        {
            "created_at": "2025-11-13T17:11:34.568639",
            "id": 1985,
            "item_total": 99.92,
            "product": {
                "category": "Electronics",
                "created_at": "2025-09-28T00:17:15.200501",
                "description": "Updated description",
                "id": 4,
                "image_url": "https://picsum.photos/400/300?random=4",
                "name": "4K Monitor 27\"",
                "price": 24.98,
                "stock": 60,
                "updated_at": "2025-11-13T16:53:40.676913"
            },
            "product_id": 4,
            "quantity": 4,
            "updated_at": "2025-11-13T17:12:00.682576",
            "user_id": 120
        }
    ],
    "success": true,
    "total": 99.92
}
```
**Response (200): Empty Cart**
```json
{
    "count": 0,
    "data": [],
    "success": true,
    "total": 0
}
```


---

### Update Cart Item

**Endpoint:** `PUT /api/cart/items/{{item_id}}`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Request:**
```json
{
  "quantity": 3
}
```

**Response (200):**
```json
{
    "data": {
        "created_at": "2025-11-13T17:11:34.568639",
        "id": 1985,
        "product_id": 4,
        "quantity": 3,
        "updated_at": "2025-11-13T17:16:32.033077",
        "user_id": 120
    },
    "message": "Cart item updated successfully",
    "success": true
}
```

---

### Remove Item from Cart

**Endpoint:** `DELETE /api/cart/items/{{item_id}}`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "created_at": "2025-11-13T17:11:34.568639",
        "id": 1985,
        "product_id": 4,
        "quantity": 3,
        "updated_at": "2025-11-13T17:20:46.445487",
        "user_id": 120
    },
    "message": "Item removed from cart successfully",
    "success": true
}
```

**Response (404): if product not exist in cart**
```json
{
    "error": "Cart item not found",
    "success": false
}
```

---
## 📦 Order Management : need products in cart as pre-conditions

### Create Order

**Endpoint:** `POST /api/orders`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Request:**
```json
{
"shipping_address": "123 Test Street"
}
```

**Response (201):**
```json
{
    "data": {
        "created_at": "2025-11-13T17:31:21.210470",
        "id": 101,
        "items": [
            {
                "price": 59.99,
                "product_id": 5,
                "product_name": "USB-C Hub",
                "quantity": 3,
                "subtotal": 179.97
            }
        ],
        "shipping_address": "123 Test Street",
        "status": "pending",
        "total_amount": 179.97,
        "user_id": 120
    },
    "message": "Order created successfully",
    "success": true
}
```

**Response (400): Bad Request : pre-conditon cart should have products**
```json
{
    "error": "Cart is empty",
    "success": false
}
```


**Request:**
```json
{

}
```
**Response (400): Bad Request : Empty Ship Address** new
```json
{
    "error": "Shipping address is required",
    "success": false
}
```


---

### Get User Orders

**Endpoint:** `GET /api/orders`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "count": 1,
    "data": [
        {
            "created_at": "2025-11-13T17:31:21.210470",
            "id": 101,
            "items": [
                {
                    "price": 59.99,
                    "product_id": 5,
                    "product_name": "USB-C Hub",
                    "quantity": 3,
                    "subtotal": 179.97
                }
            ],
            "shipping_address": "123 Test Street",
            "status": "pending",
            "total_amount": 179.97,
            "user_id": 120
        }
    ],
    "success": true
}
```

---

### Get Order by ID

**Endpoint:** `GET /api/orders/{{order_id}}`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "created_at": "2025-11-13T17:31:21.210470",
        "id": 101,
        "items": [
            {
                "price": 59.99,
                "product_id": 5,
                "product_name": "USB-C Hub",
                "quantity": 3,
                "subtotal": 179.97
            }
        ],
        "shipping_address": "123 Test Street",
        "status": "pending",
        "total_amount": 179.97,
        "user_id": 120
    },
    "success": true
}
```

**Response (404): if order not exist**
```json
{
    "error": "Order not found",
    "success": false
}
```
ex: orderid:31
**Response (403) forbidden: if user try to access another user order** new
```json
{
    "error": "Unauthorized",
    "success": false
}
```
---

### Update Order (Shipping Address)

**Endpoint:** `PUT /api/orders/{{order_id}}`

**Headers:**
```
Authorization: Bearer {{user_token}} or {{admin_token}}
Content-Type: application/json
```

**Request:**
```json
{
  "shipping_address": "456 alex iti, City, State 1234"
}
```

**Response (200):**
```json
{
    "data": {
        "created_at": "2025-11-13T17:31:21.210470",
        "id": 101,
        "items": [
            {
                "price": 59.99,
                "product_id": 5,
                "product_name": "USB-C Hub",
                "quantity": 3,
                "subtotal": 179.97
            }
        ],
        "shipping_address": "456 alex iti, City, State 1234",
        "status": "processing",
        "total_amount": 179.97,
        "updated_at": "2025-11-13T17:45:28.374688",
        "user_id": 120
    },
    "message": "Order updated successfully",
    "success": true
}
```

**Response (404): if order not exist**
```json
{
    "error": "Order not found",
    "success": false
}
```
---

### Update Order Status (Admin Only)

**Endpoint:** `PUT /api/orders/{{order_id}}/status`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Request:**
```json
{
  "status": "processing"
}
```

**Valid statuses:** `pending`, `processing`, `shipped`, `delivered`, `cancelled`

**Response (200): if order status updated**
```json
{
    "data": {
        "created_at": "2025-11-13T17:49:42.829863",
        "id": 102,
        "items": [
            {
                "price": 59.99,
                "product_id": 5,
                "product_name": "USB-C Hub",
                "quantity": 3,
                "subtotal": 179.97
            }
        ],
        "shipping_address": "123 Test Street",
        "status": "processing",
        "total_amount": 179.97,
        "updated_at": "2025-11-13T17:49:54.350365",
        "user_id": 120
    },
    "message": "Order status updated successfully",
    "success": true
}


```

**Response (200): if order status not updated**
```json
{
    "data": {
        "created_at": "2025-11-13T17:49:42.829863",
        "id": 102,
        "items": [
            {
                "price": 59.99,
                "product_id": 5,
                "product_name": "USB-C Hub",
                "quantity": 3,
                "subtotal": 179.97
            }
        ],
        "shipping_address": "123 Test Street",
        "status": "processing",
        "total_amount": 179.97,
        "updated_at": "2025-11-13T17:49:54.350365",
        "user_id": 120
    },
    "message": "Order status unchanged",
    "success": true
}
```

**Responses(200,400): when change from processing and to other states** new
```json
pending : 
    "error": "Cannot transition from processing to pending. Allowed: shipped, cancelled",
    "success": false
shipped:
"message": "Order status updated successfully",
    "success": true
delivered:
  "message": "Order status updated successfully",
    "success": true
cancelled:
    "error": "Cannot transition from delivered to cancelled. Allowed: ",
    "success": false
```


**Request: if invalid status**
```json
{
  "status": "invalid_status"
}
```
**Responses(400): if invalid status** new
```json
{
    "error": "Invalid status",
    "success": false
}
```

**Responses(403) forbidden: if non admin try to change state** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```
---

### Cancel Order

**Endpoint:** `DELETE /api/orders/{{order_id}}`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Bearer {{user_token}} can cancle pending orders
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "cancelled_at": "2025-11-13T17:53:11.071894",
        "cart_restored": true,
        "created_at": "2025-11-13T17:49:42.829863",
        "id": 102,
        "items": [
            {
                "price": 59.99,
                "product_id": 5,
                "product_name": "USB-C Hub",
                "quantity": 3,
                "subtotal": 179.97
            }
        ],
        "shipping_address": "123 Test Street",
        "status": "cancelled",
        "total_amount": 179.97,
        "updated_at": "2025-11-13T17:49:54.350365",
        "user_id": 120
    },
    "items_restored": 1,
    "message": "Order cancelled successfully. Items restored to cart.",
    "success": true
}
```

**Response (400): bad request if order is not in pending status** new
```json
{
    "error": "Cannot cancel this order",
    "success": false
}
```
**Response (400): bad request if user try to cancel non-pending order** new
```json
{
    "error": "Cannot cancel this order. Allowed statuses: pending",
    "success": false
}
```



---

### Get Orders by Status

**Endpoint:** `GET /api/orders/status/cancelled`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "count": 4,
    "data": [
        {
            "created_at": "2025-11-13T17:31:21.210470",
            "id": 101,
            "items": [
                {
                    "price": 59.99,
                    "product_id": 5,
                    "product_name": "USB-C Hub",
                    "quantity": 3,
                    "subtotal": 179.97
                }
            ],
            "shipping_address": "456 alex iti, City, State 1234",
            "status": "cancelled",
            "total_amount": 179.97,
            "updated_at": "2025-11-13T17:48:59.919990",
            "user_id": 120
        },
        {
            "cancelled_at": "2025-11-13T17:53:11.071894",
            "cart_restored": true,
            "created_at": "2025-11-13T17:49:42.829863",
            "id": 102,
            "items": [
                {
                    "price": 59.99,
                    "product_id": 5,
                    "product_name": "USB-C Hub",
                    "quantity": 3,
                    "subtotal": 179.97
                }
            ],
            "shipping_address": "123 Test Street",
            "status": "cancelled",
            "total_amount": 179.97,
            "updated_at": "2025-11-13T17:49:54.350365",
            "user_id": 120
        },
        {
            "cancelled_at": "2025-11-13T18:16:19.443026",
            "cart_restored": true,
            "created_at": "2025-11-13T18:15:59.208935",
            "id": 103,
            "items": [
                {
                    "price": 59.99,
                    "product_id": 5,
                    "product_name": "USB-C Hub",
                    "quantity": 3,
                    "subtotal": 179.97
                }
            ],
            "shipping_address": "456 alex iti, City, State 1234",
            "status": "cancelled",
            "total_amount": 179.97,
            "updated_at": "2025-11-13T18:16:14.105718",
            "user_id": 120
        },
        {
            "cancelled_at": "2025-11-13T18:16:59.481696",
            "cart_restored": true,
            "created_at": "2025-11-13T18:16:52.833101",
            "id": 104,
            "items": [
                {
                    "price": 59.99,
                    "product_id": 5,
                    "product_name": "USB-C Hub",
                    "quantity": 3,
                    "subtotal": 179.97
                }
            ],
            "shipping_address": "123 Test Street",
            "status": "cancelled",
            "total_amount": 179.97,
            "user_id": 120
        }
    ],
    "success": true
}
```

---

### Export Orders (Admin Only)

**Endpoint:** `GET /api/export/orders`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Query Parameters:**
```
start_date=2025-10-01
end_date=2025-10-10
```

**Response (200):**
```json
{
    "data": {
        "export_date": "2025-11-13T18:24:01.208701",
        "orders": [
            {
                "created_at": "2025-10-08T00:17:15.201713",
                "id": 6,
                "items": [
                    {
                        "price": 89.99,
                        "product_id": 55,
                        "product_name": "Tool Set",
                        "quantity": 1,
                        "subtotal": 89.99
                    }
                ],
                "shipping_address": "603 Maple Dr, Houston, CA 96721",
                "status": "delivered",
                "total_amount": 89.99,
                "updated_at": "2025-10-11T00:17:15.201713",
                "user_id": 16
            },
            {
                "created_at": "2025-10-06T00:17:15.201713",
                "id": 11,
                "items": [
                    {
                        "price": 19.99,
                        "product_id": 14,
                        "product_name": "HDMI Cable 10ft",
                        "quantity": 2,
                        "subtotal": 39.98
                    },
                    {
                        "price": 199.99,
                        "product_id": 18,
                        "product_name": "Leather Jacket",
                        "quantity": 2,
                        "subtotal": 399.98
                    }
                ],
                "shipping_address": "446 Main St, Houston, CA 53115",
                "status": "pending",
                "total_amount": 439.96,
                "user_id": 22
            },
            {
                "created_at": "2025-10-10T00:17:15.201713",
                "id": 14,
                "items": [
                    {
                        "price": 27.99,
                        "product_id": 35,
                        "product_name": "Fitness & Nutrition",
                        "quantity": 2,
                        "subtotal": 55.98
                    },
                    {
                        "price": 49.99,
                        "product_id": 15,
                        "product_name": "Laptop Stand",
                        "quantity": 1,
                        "subtotal": 49.99
                    }
                ],
                "shipping_address": "394 Oak Ave, Indianapolis, NY 88148",
                "status": "shipped",
                "total_amount": 105.97,
                "updated_at": "2025-10-10T00:17:15.201713",
                "user_id": 11
            },
            {
                "created_at": "2025-10-06T00:17:15.201713",
                "id": 20,
                "items": [
                    {
                        "price": 39.99,
                        "product_id": 50,
                        "product_name": "Storage Bins Set",
                        "quantity": 1,
                        "subtotal": 39.99
                    }
                ],
                "shipping_address": "700 Main St, San Antonio, CA 95466",
                "status": "delivered",
                "total_amount": 39.99,
                "updated_at": "2025-10-11T00:17:15.201713",
                "user_id": 5
            },
            {
                "created_at": "2025-10-06T00:17:15.201713",
                "id": 22,
                "items": [
                    {
                        "price": 34.99,
                        "product_id": 65,
                        "product_name": "Basketball",
                        "quantity": 1,
                        "subtotal": 34.99
                    },
                    {
                        "price": 199.99,
                        "product_id": 18,
                        "product_name": "Leather Jacket",
                        "quantity": 3,
                        "subtotal": 599.97
                    },
                    {
                        "price": 19.99,
                        "product_id": 16,
                        "product_name": "Classic T-Shirt",
                        "quantity": 2,
                        "subtotal": 39.98
                    },
                    {
                        "price": 59.99,
                        "product_id": 5,
                        "product_name": "USB-C Hub",
                        "quantity": 3,
                        "subtotal": 179.97
                    },
                    {
                        "price": 79.99,
                        "product_id": 28,
                        "product_name": "Bomber Jacket",
                        "quantity": 1,
                        "subtotal": 79.99
                    }
                ],
                "shipping_address": "742 Maple Dr, San Jose, NY 70312",
                "status": "processing",
                "total_amount": 934.9,
                "user_id": 28
            },
            {
                "created_at": "2025-10-04T00:17:15.201713",
                "id": 31,
                "items": [
                    {
                        "price": 34.99,
                        "product_id": 65,
                        "product_name": "Basketball",
                        "quantity": 3,
                        "subtotal": 104.97
                    },
                    {
                        "price": 149.99,
                        "product_id": 3,
                        "product_name": "Mechanical Keyboard",
                        "quantity": 1,
                        "subtotal": 149.99
                    }
                ],
                "shipping_address": "941 Sunset Blvd, Columbus, TX 87725",
                "status": "delivered",
                "total_amount": 254.96,
                "updated_at": "2025-10-06T00:17:15.201713",
                "user_id": 26
            },
            {
                "created_at": "2025-10-02T00:17:15.202713",
                "id": 32,
                "items": [
                    {
                        "price": 54.99,
                        "product_id": 22,
                        "product_name": "Cargo Pants",
                        "quantity": 3,
                        "subtotal": 164.97
                    },
                    {
                        "price": 38.99,
                        "product_id": 44,
                        "product_name": "Philosophy Essentials",
                        "quantity": 3,
                        "subtotal": 116.97
                    }
                ],
                "shipping_address": "505 Maple Dr, Charlotte, FL 47748",
                "status": "delivered",
                "total_amount": 281.94,
                "updated_at": "2025-10-14T00:17:15.202713",
                "user_id": 30
            },
            {
                "created_at": "2025-10-06T00:17:15.202713",
                "id": 37,
                "items": [
                    {
                        "price": 69.99,
                        "product_id": 30,
                        "product_name": "Wool Sweater",
                        "quantity": 1,
                        "subtotal": 69.99
                    },
                    {
                        "price": 39.99,
                        "product_id": 57,
                        "product_name": "Wall Clock",
                        "quantity": 3,
                        "subtotal": 119.97
                    },
                    {
                        "price": 39.99,
                        "product_id": 13,
                        "product_name": "Power Bank 20000mAh",
                        "quantity": 1,
                        "subtotal": 39.99
                    }
                ],
                "shipping_address": "505 Maple Dr, Charlotte, FL 47748",
                "status": "processing",
                "total_amount": 229.95,
                "user_id": 30
            },
            {
                "created_at": "2025-10-02T00:17:15.202713",
                "id": 44,
                "items": [
                    {
                        "price": 39.99,
                        "product_id": 75,
                        "product_name": "Fitness Tracker",
                        "quantity": 2,
                        "subtotal": 79.98
                    },
                    {
                        "price": 59.99,
                        "product_id": 73,
                        "product_name": "Badminton Set",
                        "quantity": 2,
                        "subtotal": 119.98
                    },
                    {
                        "price": 24.99,
                        "product_id": 69,
                        "product_name": "Water Bottle 32oz",
                        "quantity": 1,
                        "subtotal": 24.99
                    },
                    {
                        "price": 34.99,
                        "product_id": 21,
                        "product_name": "Polo Shirt",
                        "quantity": 1,
                        "subtotal": 34.99
                    }
                ],
                "shipping_address": "941 Sunset Blvd, Columbus, TX 87725",
                "status": "processing",
                "total_amount": 259.94,
                "user_id": 26
            }
        ],
        "period": {
            "end_date": "2025-10-10",
            "start_date": "2025-10-01"
        },
        "total_orders": 9
    },
    "success": true
}
```
**Response (403): if user try to export order:** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```
---


## ⭐ Reviews & Ratings
## need Create Product (Pre-Condition)

### Create Review 

**Endpoint:** `POST /api/reviews`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "product_id": {{product_id}},
    "rating": 4,
    "comment": "Excellent product test!"
}
```

**Response (201):**
```json
{
    "data": {
        "comment": "Excellent product2!",
        "created_at": "2025-11-13T18:39:24.230296",
        "id": 129,
        "product_id": 85,
        "rating": 4,
        "user_id": 120
    },
    "message": "Review created successfully",
    "success": true
}
```
**Response (404): if product not found:**
```json
{
    "error": "Product not found",
    "success": false
}
```
**Response (400): bad requst: if already reviewed**
```json
{
    "error": "You have already reviewed this product",
    "success": false
}
```
**Response (400): bad requst: if invalid rating > 5** new
```json
{
    "error": "Rating must be between 1 and 5",
    "success": false
}
```

---

### Get Product Reviews

**Endpoint:** `GET /api/products/{{product_id}}/reviews`

**Response (200):**
```json
{
    "average_rating": 4.0,
    "count": 1,
    "data": [
        {
            "comment": "Excellent product2!",
            "created_at": "2025-11-13T18:46:27.087255",
            "id": 130,
            "product_id": 88,
            "rating": 4,
            "user_id": 120
        }
    ],
    "success": true
}
```
**Response (200): no review product**
```json
{
    "average_rating": 0,
    "count": 0,
    "data": [],
    "success": true
}
```

---

### Check if User Reviewed Product [new]

**Endpoint:** `GET /api/products/{{product_id}}/reviews/check`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Response (200): if reviewed**
```json
{
    "has_reviewed": true,
    "review": {
        "comment": "Excellent product2!",
        "created_at": "2025-11-13T18:46:27.087255",
        "id": 130,
        "product_id": 88,
        "rating": 4,
        "user_id": 120
    },
    "success": true
}
```
**Response (200): if not reviewed**
```json
{
    "has_reviewed": false,
    "review": null,
    "success": true
}
```

---

## 📊 Admin & Statistics

### Get Dashboard Statistics

**Endpoint:** `GET /api/stats`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "low_stock_products": 0,
        "pending_orders": 30,
        "total_orders": 105,
        "total_products": 87,
        "total_revenue": 67078.75,
        "total_reviews": 130,
        "total_users": 115
    },
    "success": true
}
```
**Response (403)forbidden: if non-admin try to get stats** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```


### Get Dashboard Analytics

**Endpoint:** `GET /analytics/dashboard`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "monthly_revenue": 179.97,
        "page_views_data": [
            {
                "date": "2025-09-21",
                "views": 422
            },
            {
                "date": "2025-09-20",
                "views": 142
            },
            {
                "date": "2025-09-19",
                "views": 165
            },
            {
                "date": "2025-09-18",
                "views": 104
            },
            {
                "date": "2025-09-17",
                "views": 463
            },
            {
                "date": "2025-09-16",
                "views": 184
            },
            {
                "date": "2025-09-15",
                "views": 134
            }
        ],
        "popular_products": [
            {
                "orders": 12,
                "product": {
                    "category": "Electronics",
                    "created_at": "2025-09-15T00:17:15.200501",
                    "description": "High-performance laptop with 16GB RAM and 512GB SSD2",
                    "id": 1,
                    "image_url": "https://picsum.photos/400/300?random=1",
                    "name": "Laptop Pro 15\"",
                    "price": 1299.99,
                    "stock": 51,
                    "updated_at": "2025-10-14T21:22:50.472349"
                },
                "views": 245
            },
            {
                "orders": 8,
                "product": {
                    "category": "Electronics",
                    "created_at": "2025-08-22T00:17:15.200501",
                    "description": "7-in-1 USB-C hub with HDMI and ethernet",
                    "id": 5,
                    "image_url": "https://picsum.photos/400/300?random=5",
                    "name": "USB-C Hub",
                    "price": 59.99,
                    "stock": 161
                },
                "views": 189
            },
            {
                "orders": 15,
                "product": {
                    "category": "Electronics",
                    "created_at": "2025-06-25T00:17:15.200501",
                    "description": "External solid state drive 1TB",
                    "id": 10,
                    "image_url": "https://picsum.photos/400/300?random=10",
                    "name": "Portable SSD 1TB",
                    "price": 149.99,
                    "stock": 43
                },
                "views": 167
            }
        ],
        "sales_data": [
            {
                "date": "2025-09-21",
                "sales": 1617
            },
            {
                "date": "2025-09-20",
                "sales": 966
            },
            {
                "date": "2025-09-19",
                "sales": 1650
            },
            {
                "date": "2025-09-18",
                "sales": 637
            },
            {
                "date": "2025-09-17",
                "sales": 1172
            },
            {
                "date": "2025-09-16",
                "sales": 1270
            },
            {
                "date": "2025-09-15",
                "sales": 1851
            }
        ],
        "total_orders": 105,
        "total_products": 87,
        "total_revenue": 67078.75000000006,
        "total_users": 115,
        "user_registrations": [
            {
                "date": "2025-09-21",
                "registrations": 14
            },
            {
                "date": "2025-09-20",
                "registrations": 11
            },
            {
                "date": "2025-09-19",
                "registrations": 16
            },
            {
                "date": "2025-09-18",
                "registrations": 15
            },
            {
                "date": "2025-09-17",
                "registrations": 10
            },
            {
                "date": "2025-09-16",
                "registrations": 5
            },
            {
                "date": "2025-09-15",
                "registrations": 16
            }
        ]
    },
    "success": true
}
```
**Response (403)forbidden: if non-admin try to get dashboard stats** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```


### Get Sales Report

**Endpoint:** `GET /analytics/reports/sales`

**Query Parameters:**
```
start_date=2024-01-01
end_date=2026-12-31
```

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "data": {
        "orders": [
            {
                "created_at": "2025-09-12T00:17:15.200501",
                "id": 1,
                "items": [
                    {
                        "price": 39.99,
                        "product_id": 50,
                        "product_name": "Storage Bins Set",
                        "quantity": 2,
                        "subtotal": 79.98
                    },
                    {
                        "price": 64.99,
                        "product_id": 60,
                        "product_name": "Garden Tools Kit",
                        "quantity": 1,
                        "subtotal": 64.99
                    },
                    {
                        "price": 14.99,
                        "product_id": 64,
                        "product_name": "Jump Rope",
                        "quantity": 3,
                        "subtotal": 44.97
                    },
                    {
                        "price": 29.99,
                        "product_id": 2,
                        "product_name": "Wireless Mouse",
                        "quantity": 3,
                        "subtotal": 89.97
                    },
                    {
                        "price": 24.99,
                        "product_id": 33,
                        "product_name": "Science Fiction Anthology",
                        "quantity": 3,
                        "subtotal": 74.97
                    }
                ],
                "shipping_address": "700 Main St, San Antonio, CA 95466",
                "status": "delivered",
                "total_amount": 354.88,
                "updated_at": "2025-09-27T00:17:15.201713",
                "user_id": 5
            },
            {
                "created_at": "2025-09-15T00:17:15.201713",
                "id": 2,
                "items": [
                    {
                        "price": 39.99,
                        "product_id": 31,
                        "product_name": "Python Programming Guide",
                        "quantity": 1,
                        "subtotal": 39.99
                    },
                    {
                        "price": 32.99,
                        "product_id": 37,
                        "product_name": "Graphic Design Basics",
                        "quantity": 3,
                        "subtotal": 98.97
                    }
                ],
                "shipping_address": "880 Washington St, Seattle, FL 17234",
                "status": "shipped",
                "total_amount": 138.96,
                "updated_at": "2025-09-26T00:17:15.201713",
                "user_id": 8
            },
           ........
        "period": {
            "end_date": "2025-10-10",
            "start_date": "2024-01-01"
        },
        "sales_by_status": {
            "cancelled": {
                "count": 3,
                "revenue": 0
            },
            "delivered": {
                "count": 13,
                "revenue": 7614.26
            },
            "pending": {
                "count": 5,
                "revenue": 2316.63
            },
            "processing": {
                "count": 9,
                "revenue": 3297.42
            },
            "shipped": {
                "count": 18,
                "revenue": 6886.03
            }
        },
        "summary": {
            "average_order_value": 419.0487499999999,
            "cancelled_orders": 3,
            "total_orders": 48,
            "total_sales": 20114.339999999997
        }
    },
    "success": true
}
```
**Response (403)forbidden: if non-admin try to get sales report** new
```json
{
    "error": "Admin privileges required",
    "success": false
}


---
```
## 📋 Extended API Endpoints

### Help & FAQ System


#### Create Help Article (Admin Only)

**Endpoint:** `POST /api/help`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "question": "How to track my order2?",
    "answer": "Use the orders page to check status2.",
    "category": "Orders2"
}
```

**Response (201):**
```json
{
    "message": "Article created successfully",
    "success": true
}
```
**Response (403)forbidden: if non-admin try to create article:**
```json
{
    "error": "Admin privileges required",
    "success": false
}
```
---


#### Get Help Categories

**Endpoint:** `GET /api/help/categories`

**Response (200):**
```json
{
    "data": [
        "Payment",
        "Orders",
        "Shipping",
        "General",
        "Returns",
        "Test",
        "Orders2"
    ],
    "success": true
}
```

---
#### List Help Articles

**Endpoint:** `GET /api/help`

**Query Parameters:**
```
category=Orders2
page=1
per_page=10
```

**Response (200):**
```json
{
    "count": 4,
    "data": [
        {
            "answer": "Use the orders page to check status2.",
            "category": "Orders2",
            "created_at": "2025-10-19T23:12:17.499126",
            "helpful_count": 0,
            "id": 33,
            "question": "How to track my order2?"
        },
        {
            "answer": "Use the orders page to check status2.",
            "category": "Orders2",
            "created_at": "2025-11-13T19:21:08.641411",
            "helpful_count": 0,
            "id": 35,
            "question": "How to track my order2?"
        },
        {
            "answer": "Use the orders page to check status2.",
            "category": "Orders2",
            "created_at": "2025-11-13T19:23:14.695747",
            "helpful_count": 0,
            "id": 36,
            "question": "How to track my order2?"
        },
        {
            "answer": "Use the orders page to check status2.",
            "category": "Orders2",
            "created_at": "2025-11-13T19:23:37.807678",
            "helpful_count": 0,
            "id": 37,
            "question": "How to track my order2?"
        }
    ],
    "success": true
}
```

---
#### Get Help Articles by ID

**Endpoint:** `GET /api/help/{{help_id}}`


**Response (200):**
```json
{
    "data": {
        "answer": "Use the orders page to check status2.",
        "category": "Orders2",
        "created_at": "2025-11-13T19:23:37.807678",
        "helpful_count": 0,
        "id": 37,
        "question": "How to track my order2?"
    },
    "success": true
}
```
**Response (404): if article not found**
```json
{
    "error": "Article not found",
    "success": false
}
```
---

#### Mark Article Helpful

**Endpoint:** `POST /api/help/{{help_id}}/helpful`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {{token}} (optional - uses IP if not provided)
```


**Response (200):**
```json
{
    "message": "Thank you for your feedback!",
    "success": true
}
```


**Response (400): if article already marked helpful**
```json
{
    "already_helpful": true,
    "error": "You have already marked this article as helpful",
    "success": false
}
```


**Response (404): Article not found**
```json
{
    "success": false,
    "error": "Article not found"
}
```
---

#### Update Help Article

**Endpoint:** `PUT /api/help/{{help_id}}`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {{token}} 
```

**Request:**
```json
{
    "question": "How to track my order?",
    "answer": "Visit the orders page and use the tracking link.",
    "category": "Orders"
}
```

**Response (200):**
```json
{
    "message": "Article updated successfully",
    "success": true
}
```


**Response (404): Article not found**
```json
{
    "error": "Article not found",
    "success": false
}
```

---


### Contact System

#### Submit Contact Message

**Endpoint:** `POST /api/contact`

**Request:**
```json
{
    "name": "Mo Gomaa",
    "email": "iti@example.com",
    "subject": "Order issue Test",
    "message": "I need help with my order Test."
}
```

**Response (201):**
```json
{
    "message": "Your message has been submitted successfully. We will get back to you soon!",
    "success": true
}
```
**Request: missing fields**
```json
{"name": "Test"}
```

**Response (400)Bad Request: missing field response** new
```json
{
    "error": "Name, email, and message are required",
    "success": false
}
```

---

#### Get Contact Messages (Admin Only)

**Endpoint:** `GET /api/contact/messages`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```


**Query**
```
status=pending
```


**Response (200):**
```json
{
    "count": 5,
    "data": [
        {
            "created_at": "2025-10-14T00:22:36.660997",
            "email": "john.smith@email.com",
            "id": 1,
            "message": "I'm interested in your electronics products. Do you have any discounts available?",
            "name": "John Smith",
            "status": "pending",
            "subject": "Product Inquiry"
        },
        {
            "created_at": "2025-10-14T21:19:49.808408",
            "email": "010288@gmail.com",
            "id": 11,
            "message": "dfwef",
            "name": "tt",
            "status": "pending",
            "subject": "General Inquiry"
        },
        {
            "created_at": "2025-11-13T19:54:06.861972",
            "email": "iti@example.com",
            "id": 18,
            "message": "I need help with my order Test.",
            "name": "Mo Gomaa",
            "status": "pending",
            "subject": "Order issue Test"
        },
        {
            "created_at": "2025-11-13T19:54:37.069385",
            "email": "iti@example.com",
            "id": 19,
            "message": "I need help with my order Test.",
            "name": "Mo Gomaa",
            "status": "pending",
            "subject": "Order issue Test"
        },
        {
            "created_at": "2025-11-13T19:55:20.180750",
            "email": "iti@example.com",
            "id": 20,
            "message": "I need help with my order Test.",
            "name": "Mo Gomaa",
            "status": "pending",
            "subject": "Order issue Test"
        }
    ],
    "success": true
}
```

**Response (403)forbidden: if non-admin try to get messages:** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```
---

---

#### Respond to Contact Message (Admin Only)


**Endpoint:** `POST /api/contact/messages/{{contact_message_id}}/respond`

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```


**Request:**
```json
{
    "response": "Thanks for reaching out Test. Your issue is resolved."
}
```

**Response (200):**
```json
{
    "message": "Response sent successfully",
    "success": true
}
```
**Response (404): if message not found** new
```json
{
    "error": "Message not found",
    "success": false
}
```
**Response (403)forbidden: if user try to response to contanct** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```
### Wishlist System

#### Add to Wishlist
### List Users[Pre-Conditon1]
### List Products [Pre-Conditon2]

**Endpoint:** `POST /api/wishlist`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "user_id": {{user_id}},
    "product_id": {{product_id}}
}
```

**Response (201):**
```json
{
    "message": "Product added to wishlist successfully",
    "success": true
}
```
**Response (404): if product not found**
```json
  {
    "error": "Product not found",
    "success": false
}
```
**Response (400): if product already in wishlist**
```json
{
    "error": "Product already in wishlist",
    "success": false
}
```
---
#### Get Wishlist

**Endpoint:** `GET /api/wishlist`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "count": 1,
    "data": [
        {
            "created_at": "2025-11-13T20:15:36.802864",
            "id": 7,
            "product": {
                "category": "Electronics",
                "created_at": "2025-06-25T00:17:15.200501",
                "description": "External solid state drive 1TB",
                "id": 10,
                "image_url": "https://picsum.photos/400/300?random=10",
                "name": "Portable SSD 1TB",
                "price": 149.99,
                "stock": 43
            },
            "product_id": 10,
            "user_id": 120
        }
    ],
    "success": true
}
```

---


#### Remove from Wishlist

**Endpoint:** `DELETE /api/wishlist/{{item_id}}`

**Headers:**
```
Authorization: Bearer {{user_token}}
Content-Type: application/json
```

**Response (200):**
```json
{
    "message": "Product removed from wishlist successfully",
    "success": true
}
```
**Response (404): if wishlist not found**
```json
{
    "error": "Wishlist item not found",
    "success": false
}
```




## Coupons

### Create Coupon (Admin)

**Endpoint:** `POST /api/coupons

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "code": "{{code}}",
    "description": "10% off first order",
    "discount_type": "percentage",
    "discount_value": 10,
    "min_order_amount": 50,
    "max_discount": 30,
    "usage_limit": 100
}
```

**Response (201):**
```json
{
    "data": {
        "code": "xkvde8zx10",
        "created_at": "2025-11-13T20:32:11.303221",
        "description": "10% off first order",
        "discount_type": "percentage",
        "discount_value": 10,
        "expires_at": "2025-12-13T20:32:11.303221",
        "id": 24,
        "is_active": true,
        "max_discount": 30,
        "min_order_amount": 50,
        "usage_limit": 100,
        "used_count": 0
    },
    "message": "Coupon created successfully",
    "success": true
}
```

**Request:**
```json
    {
    "code": "{{code}}",
    "expiry_date": "2026-12-31",
    "type": "percentage",
    "discount": 15
     }

```
**Response (400) bad request: missing fields** new
```json
{
    "error": "Missing required fields",
    "success": false
}


```
**Response (403) forbidden: user try create coupon** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```
**Response (400) bad request: when code with same name already created** new
```json
{
    "error": "Coupon code already exists",
    "success": false
}
```

---



### Validate Coupon


**Endpoint:** `POST /api/coupons/validate

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```

**Request:**
```json
{
    "code": "{{code}}",
    "order_amount": 120.0
}
```

**Response (200):**
```json
{
    "data": {
        "code": "00ebfvtx10",
        "coupon_id": 27,
        "description": "10% off first order",
        "discount_amount": 12.0,
        "discount_type": "percentage",
        "final_amount": 108.0
    },
    "success": true
}
```
**Response (404): wrong coupon**
```json
{
    "error": "Invalid coupon code",
    "success": false
}
```
**Request:**
```json
{
    "code": "EXPIRED",
    "order_amount": 120.0
}
```
**Response (400)bad request: Expire Coupon** new
```json
{
    "error": "Coupon has expired",
    "success": false
}
```
---



### List Coupons


**Endpoint:** `GET /api/coupons

**Headers:**
```
Authorization: Bearer {{admin_token}}
Content-Type: application/json
```


**Response (200):**
```json
{
    "count": 19,
    "data": [
        {
            "code": "6wchuxpg10",
            "created_at": "2025-10-14T20:58:31.692728",
            "description": "10% off first order",
            "discount_type": "percentage",
            "discount_value": 10,
            "expires_at": "2025-11-13T20:58:31.692728",
            "id": 9,
            "is_active": true,
            "max_discount": 30,
            "min_order_amount": 50,
            "usage_limit": 100,
            "used_count": 0
        },
        {
            "code": "hykyomb110",
            "created_at": "2025-10-14T21:15:31.897706",
            "description": "10% off first order",
            "discount_type": "percentage",
            "discount_value": 10,
            "expires_at": "2025-11-13T21:15:31.897706",
            "id": 10,
            "is_active": true,
            "max_discount": 30,
            "min_order_amount": 50,
            "usage_limit": 100,
            "used_count": 0
        },
        {
            "code": "qm03br3010",
            "created_at": "2025-10-14T21:47:22.053634",
            "description": "10% off first order",
            "discount_type": "percentage",
            "discount_value": 10,
            "expires_at": "2025-11-13T21:47:22.053634",
            "id": 11,
            "is_active": true,
            "max_discount": 30,
            "min_order_amount": 50,
            "usage_limit": 100,
            "used_count": 0
        }
    ],
    "success": true
}
```
**Response (403)forbidden: if non-admin try to get coupons** new
```json
{
    "error": "Admin privileges required",
    "success": false
}
```

---



## Notifications
### create random notifications

**Endpoint:** `POST /notifications/test-create`

**Headers:**
```
Authorization: Bearer {{admin_token}} or {{user_token}}
Content-Type: application/json
```
**Request:**
```json
{
    "count":3
}
```
**Response (201):**
```json
{
    "count": 3,
    "data": [
        {
            "body": "New Message: This is a test notification at 2025-11-17T04:34:10.595780",
            "created_at": "2025-11-17T04:34:10.595780",
            "id": 27,
            "is_read": false,
            "title": "New Message",
            "user_id": 165
        },
        {
            "body": "System Alert: This is a test notification at 2025-11-17T04:34:10.595780",
            "created_at": "2025-11-17T04:34:10.595780",
            "id": 28,
            "is_read": false,
            "title": "System Alert",
            "user_id": 165
        },
        {
            "body": "Flash Sale: This is a test notification at 2025-11-17T04:34:10.595780",
            "created_at": "2025-11-17T04:34:10.595780",
            "id": 29,
            "is_read": false,
            "title": "Flash Sale",
            "user_id": 165
        }
    ],
    "message": "Created 3 test notification(s)",
    "success": true
}
```
### List Notifications

**Endpoint:** `GET /notifications

**Headers:**
```
Authorization: Bearer {{admin_token}} or {{user_token}}
Content-Type: application/json
```

**Response (201):**
```json
{
    "count": 3,
    "data": [
        {
            "created_at": "2025-11-13T11:00:00.000000",
            "id": 5,
            "is_read": false,
            "message": "Your order has been confirmed and is being processed.",
            "title": "Order Confirmed",
            "type": "order_update",
            "user_id": 40
        },
        {
            "created_at": "2025-11-13T10:00:00.000000",
            "id": 4,
            "is_read": false,
            "message": "Thank you for joining us. Enjoy shopping!",
            "title": "Welcome to Our Store!",
            "type": "welcome",
            "user_id": 40
        },
        {
            "created_at": "2025-11-12T15:00:00.000000",
            "id": 6,
            "is_read": true,
            "message": "Don't miss our flash sale! Up to 50% off selected items.",
            "read_at": "2025-11-13T09:00:00.000000",
            "title": "Flash Sale Alert",
            "type": "promotion",
            "user_id": 40
        }
    ],
    "success": true,
    "unread_count": 2
}
```


### Mark Notification Read

**Endpoint:** `PUT /notifications/{{notification_id}}/read

**Headers:**
```
Authorization: Bearer {{admin_token}} or {{user_token}}
Content-Type: application/json
```


**Response (201):**
```json
{
    "message": "Notification marked as read",
    "success": true
}
```
**Response (404): non exist notification id** new
```json
{
    "error": "Notification not found",
    "success": false
}
```
### Mark Mark All Notifications Read

**Endpoint:** `PUT /notifications/read-all

**Headers:**
```
Authorization: Bearer {{admin_token}} or {{user_token}}
Content-Type: application/json
```


**Response (200):**
```json
{
    "message": "2 notifications marked as read",
    "success": true
}
```




---









## Search & Recommendations
### Advanced Search

**Endpoint:** `GET /search/advanced`

**Query**
```
q=mouse
category=10
category=Electronics
min_price=1
max_price=500
min_rating=4
sort_by=price
sort_orde=asc
```


**Response (200):**
```json
{
    "count": 1,
    "data": [
        {
            "average_rating": 4.666666666666667,
            "category": "Electronics",
            "created_at": "2025-07-12T00:17:15.200501",
            "description": "Ergonomic wireless mouse with precision tracking",
            "id": 2,
            "image_url": "https://picsum.photos/400/300?random=2",
            "name": "Wireless Mouse",
            "price": 24.98,
            "stock": 59,
            "updated_at": "2025-11-13T16:53:29.618847"
        }
    ],
    "filters_applied": {
        "category": "Electronics",
        "max_price": 500.0,
        "min_price": 1.0,
        "min_rating": 4.0,
        "query": "mouse",
        "sort_by": "price",
        "sort_order": "asc"
    },
    "success": true
}

```



---
### Product Recommendations

**Endpoint:** `GET /recommendations/1`



**Response (200):**
```json
{
    "count": 5,
    "data": [
        {
            "category": "Electronics",
            "created_at": "2025-09-24T00:17:15.200501",
            "description": "Android tablet with 64GB storage",
            "id": 12,
            "image_url": "https://picsum.photos/400/300?random=12",
            "name": "Tablet 10\"",
            "price": 299.99,
            "stock": 169
        },
        {
            "category": "Electronics",
            "created_at": "2025-06-28T00:17:15.200501",
            "description": "Fitness tracker smart watch with heart rate monitor",
            "id": 11,
            "image_url": "https://picsum.photos/400/300?random=11",
            "name": "Smart Watch",
            "price": 249.99,
            "stock": 178
        },
        {
            "category": "Electronics",
            "created_at": "2025-05-25T00:17:15.200501",
            "description": "True wireless earbuds with active noise cancellation",
            "id": 8,
            "image_url": "https://picsum.photos/400/300?random=8",
            "name": "Wireless Earbuds",
            "price": 199.99,
            "stock": 27
        },
        {
            "category": "Electronics",
            "created_at": "2025-08-11T00:17:15.200501",
            "description": "RGB mechanical keyboard with Cherry MX switches",
            "id": 3,
            "image_url": "https://picsum.photos/400/300?random=3",
            "name": "Mechanical Keyboard",
            "price": 149.99,
            "stock": 39
        },
        {
            "category": "Electronics",
            "created_at": "2025-06-25T00:17:15.200501",
            "description": "External solid state drive 1TB",
            "id": 10,
            "image_url": "https://picsum.photos/400/300?random=10",
            "name": "Portable SSD 1TB",
            "price": 149.99,
            "stock": 43
        }
    ],
    "success": true
}

```

**Endpoint:** `GET /recommendations/99999`



**Response (404): non existing product** new
```json
{
    "error": "Product not found",
    "success": false
}
```

---
### User Recommendations

**Endpoint:** `GET /recommendations/user/{{user_id}}`



**Response (200):**
```json
{
    "count": 3,
    "data": [
        {
            "category": "Electronics",
            "created_at": "2025-09-15T00:17:15.200501",
            "description": "High-performance laptop with 16GB RAM and 512GB SSD2",
            "id": 1,
            "image_url": "https://picsum.photos/400/300?random=1",
            "name": "Laptop Pro 15\"",
            "price": 1299.99,
            "stock": 51,
            "updated_at": "2025-10-14T21:22:50.472349"
        },
        {
            "category": "Electronics",
            "created_at": "2025-08-22T00:17:15.200501",
            "description": "7-in-1 USB-C hub with HDMI and ethernet",
            "id": 5,
            "image_url": "https://picsum.photos/400/300?random=5",
            "name": "USB-C Hub",
            "price": 59.99,
            "stock": 152
        },
        {
            "category": "Electronics",
            "created_at": "2025-06-25T00:17:15.200501",
            "description": "External solid state drive 1TB",
            "id": 10,
            "image_url": "https://picsum.photos/400/300?random=10",
            "name": "Portable SSD 1TB",
            "price": 149.99,
            "stock": 43
        }
    ],
    "success": true
}

```


---


## Blog
### List Blog Posts

**Endpoint:** `GET /blog/posts`

**Query**
```
status=published
```


**Response (200):**
```json
{
    "count": 2,
    "data": [
        {
            "author": "Tech Team",
            "content": "Discover the latest trends in electronics and technology...",
            "created_at": "2025-10-14T00:22:36.663056",
            "excerpt": "Explore the cutting-edge electronics trends shaping 2024...",
            "featured_image": "https://picsum.photos/800/400?random=101",
            "id": 1,
            "status": "published",
            "tags": [
                "electronics",
                "trends",
                "technology"
            ],
            "title": "Top 10 Electronics Trends for 2024",
            "updated_at": "2025-10-14T00:22:36.663056",
            "views": 1253
        },
        {
            "author": "Product Team",
            "content": "A comprehensive guide to selecting the right laptop for your needs...",
            "created_at": "2025-10-14T00:22:36.663056",
            "excerpt": "Learn what to look for when buying a new laptop...",
            "featured_image": "https://picsum.photos/800/400?random=102",
            "id": 2,
            "status": "published",
            "tags": [
                "laptops",
                "buying guide",
                "computers"
            ],
            "title": "How to Choose the Perfect Laptop",
            "updated_at": "2025-10-14T00:22:36.663056",
            "views": 932
        }
    ],
    "success": true
}

```



---
### Get Blog Post

**Endpoint:** `GET /blog/posts/{{blog_post_id}}`



**Response (200):**
```json
{
    "data": {
        "author": "Product Team",
        "content": "A comprehensive guide to selecting the right laptop for your needs...",
        "created_at": "2025-10-14T00:22:36.663056",
        "excerpt": "Learn what to look for when buying a new laptop...",
        "featured_image": "https://picsum.photos/800/400?random=102",
        "id": 2,
        "status": "published",
        "tags": [
            "laptops",
            "buying guide",
            "computers"
        ],
        "title": "How to Choose the Perfect Laptop",
        "updated_at": "2025-10-14T00:22:36.663056",
        "views": 933
    },
    "success": true
}

```

**Endpoint:** `GET /blog/posts/9999`
**Response (404): non existing product**
```json
{
    "error": "Post not found",
    "success": false
}

```


---

## ⚠️ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Token missing or expired. Re-login and update `{{token}}` |
| 403 Forbidden | Not admin. Use `{{admin_token}}` for admin endpoints |
| 404 Not Found | Resource doesn't exist. Verify ID in parameters |
| 400 Bad Request | Missing required fields. Check request body |
| 409 Conflict | User already exists. Use different email |

---

## 📞 Support

For API issues:
- Check `/api/docs` for full documentation
- Review `/api/system/health` for system status
- Check response error messages
- Verify authentication token in headers

---

**Last Updated:** November 12, 2025
**API Version:** 2.0  
**Total Endpoints:** 104
**Author:** [Eng.MohamedGomaa](https://www.linkedin.com/in/gomaa2022/)