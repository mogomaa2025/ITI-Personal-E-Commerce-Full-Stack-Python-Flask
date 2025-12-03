from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps
import json
import os
import re
from datetime import datetime, timedelta
from auth import generate_token, generate_refresh_token, verify_token, hash_password, verify_password
from utils import load_json, save_json, get_next_id, validate_email, apply_price_fail, cleanup_user_data
from config import Config
from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from extended_api import register_extended_routes


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Ensure data directory exists
os.makedirs(Config.DATA_DIR, exist_ok=True)

# Initialize JSON files if they don't exist
def init_data_files():
    os.makedirs(Config.DATA_DIR, exist_ok=True)

    files = {
        'users.json': [],
        'products.json': [],
        'orders.json': [],
        'cart.json': [],
        'categories.json': [
            {"id": 1, "name": "Electronics", "description": "Electronic devices and accessories"},
            {"id": 2, "name": "Clothing", "description": "Fashion and apparel"},
            {"id": 3, "name": "Books", "description": "Books and publications"},
            {"id": 4, "name": "Home & Garden", "description": "Home improvement and garden supplies"},
            {"id": 5, "name": "Sports", "description": "Sports equipment and accessories"}
        ],
        'reviews.json': [],
        # Extended data files
        'help.json': [],
        'contact_messages.json': [],
        'wishlist.json': [],
        'coupons.json': [],
        'notifications.json': [],
        'likes.json': [],
        'helpful_votes.json': [],
        'analytics.json': {
            'popular_products': [],
            'page_views': [],
            'sales_data': [],
            'user_registrations': []
        },
        'blog_posts.json': []
    }
    
    for filename, default_data in files.items():
        filepath = os.path.join(Config.DATA_DIR, filename)
        if not os.path.exists(filepath):
            save_json(filename, default_data)

init_data_files()

# Register extended API routes
register_extended_routes(app)

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'success': False, 'error': 'Token is missing'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        user_data = verify_token(token)
        if not user_data:
            return jsonify({'success': False, 'error': 'Token is invalid or expired'}), 401
        
        return f(user_data, *args, **kwargs)
    
    return decorated

# Admin check decorator
def admin_required(f):
    @wraps(f)
    def decorated(user_data, *args, **kwargs):
        if not user_data.get('is_admin', False):
            return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
        return f(user_data, *args, **kwargs)
    return decorated

# ============== HEALTH CHECK ==============
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'API is running',
        'timestamp': datetime.now().isoformat()
    }), 200


# ============== USER MANAGEMENT ==============
@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400
    
    if not validate_email(data['email']):
        return jsonify({'success': False, 'error': 'Invalid email format'}), 400
    
    # PASSWORD VALIDATION: Enforce minimum strength requirements
    password = data['password']
    if len(password) < 6:
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters long'}), 400
    if not any(c.isdigit() for c in password):
        return jsonify({'success': False, 'error': 'Password must contain at least one number'}), 400
    if not any(c.isalpha() for c in password):
        return jsonify({'success': False, 'error': 'Password must contain at least one letter'}), 400

    # Name Validation
    name = data.get('name', '')
    if len(name) < 3:
        return jsonify({'success': False, 'error': 'Name must be at least 3 characters long'}), 400
    if not re.match(r'^[a-zA-Z\s]+$', name):
        return jsonify({'success': False, 'error': 'Name must contain only letters and spaces'}), 400

    # Phone Validation
    phone = data.get('phone', '')
    if not phone or not str(phone).strip():
        return jsonify({'success': False, 'error': 'Phone number is required'}), 400
    if not re.match(r'^[0-9+]+$', phone):
        return jsonify({'success': False, 'error': 'Phone number must contain only numbers and +'}), 400
    if len(phone) < 8 or len(phone) > 20:
        return jsonify({'success': False, 'error': 'Phone number must be between 8 and 20 characters'}), 400

    # Address Validation
    address = data.get('address', '')
    if not address or not str(address).strip():
        return jsonify({'success': False, 'error': 'Address is required'}), 400
    
    users = load_json('users.json')
    
    # Check if user already exists
    if any(u['email'] == data['email'] for u in users):
        return jsonify({'success': False, 'error': 'User already exists'}), 409
    
    new_user = {
        'id': get_next_id(users),
        'email': data['email'],
        'password': hash_password(data['password']),
        'name': data.get('name', ''),
        'phone': data.get('phone', ''),
        'address': data.get('address', ''),
        'is_admin': False,  # SECURITY FIX: Always false on registration, admin must be set manually
        'created_at': datetime.now().isoformat()
    }
    
    users.append(new_user)
    save_json('users.json', users)
    
    # Remove password from response
    user_response = {k: v for k, v in new_user.items() if k != 'password'}
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'data': user_response
    }), 201

@app.route('/api/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token using refresh token"""
    data = request.get_json()
    
    if not data or not data.get('refresh_token'):
        return jsonify({'success': False, 'error': 'Refresh token is required'}), 400
    
    refresh_token_str = data['refresh_token']
    
    # Verify refresh token
    payload = verify_token(refresh_token_str)
    if not payload:
        return jsonify({'success': False, 'error': 'Invalid or expired refresh token'}), 401
    
    # Check if token type is refresh
    if payload.get('type') != 'refresh':
        return jsonify({'success': False, 'error': 'Invalid token type'}), 401
    
    # Verify user still exists
    users = load_json('users.json')
    user = next((u for u in users if u['id'] == payload['id']), None)
    
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    # Generate new access token
    new_access_token = generate_token(user['id'], user['email'], user.get('is_admin', False))
    
    return jsonify({
        'success': True,
        'message': 'Token refreshed successfully',
        'token': new_access_token
    }), 200

@app.route('/api/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400
    
    users = load_json('users.json')
    user = next((u for u in users if u['email'] == data['email']), None)
    
    if not user or not verify_password(data['password'], user['password']):
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    # Generate both access and refresh tokens
    access_token = generate_token(user['id'], user['email'], user.get('is_admin', False))
    refresh_token = generate_refresh_token(user['id'], user['email'])
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user.get('name', ''),
            'is_admin': user.get('is_admin', False)
        }
    }), 200

@app.route('/api/users', methods=['GET'])
@token_required
@admin_required
def get_users(user_data):
    """Get all users (Admin only)"""
    users = load_json('users.json')
    
    # Remove passwords
    users_response = [{k: v for k, v in u.items() if k != 'password'} for u in users]
    
    return jsonify({
        'success': True,
        'data': users_response,
        'count': len(users_response)
    }), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_data, user_id):
    """Get user by ID"""
    # Users can only view their own profile unless they're admin
    if user_data['id'] != user_id and not user_data.get('is_admin', False):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    users = load_json('users.json')
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    user_response = {k: v for k, v in user.items() if k != 'password'}
    
    return jsonify({
        'success': True,
        'data': user_response
    }), 200

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_data, user_id):
    """Update user information"""
    if user_data['id'] != user_id and not user_data.get('is_admin', False):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    users = load_json('users.json')
    
    user_index = next((i for i, u in enumerate(users) if u['id'] == user_id), None)
    
    if user_index is None:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    # Update allowed fields
    allowed_fields = ['name', 'phone', 'address']
    for field in allowed_fields:
        if field in data:
            users[user_index][field] = data[field]
    
    users[user_index]['updated_at'] = datetime.now().isoformat()
    save_json('users.json', users)
    
    user_response = {k: v for k, v in users[user_index].items() if k != 'password'}
    
    return jsonify({
        'success': True,
        'message': 'User updated successfully',
        'data': user_response
    }), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(user_data, user_id):
    """Delete user (Admin only) and clean up all associated data"""
    users = load_json('users.json')
    
    user_index = next((i for i, u in enumerate(users) if u['id'] == user_id), None)
    
    if user_index is None:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    deleted_user = users.pop(user_index)
    save_json('users.json', users)
    
    # Clean up all user-associated data to prevent data inheritance issues
    cleanup_user_data(user_id)
    
    return jsonify({
        'success': True,
        'message': 'User deleted successfully',
        'data': {'id': deleted_user['id'], 'email': deleted_user['email']}
    }), 200

# ============== PRODUCT MANAGEMENT ==============
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering and pagination"""
    products = load_json('products.json')
    
    # Query parameters
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    search = request.args.get('search', '').lower()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Filter products
    filtered_products = products
    
    if category:
        filtered_products = [p for p in filtered_products if p.get('category') == category]
    
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p.get('price', 0) >= min_price]
    
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p.get('price', 0) <= max_price]
    
    if search:
        filtered_products = [p for p in filtered_products 
                           if search in p.get('name', '').lower() or 
                           search in p.get('description', '').lower()]
    
    # Pagination
    total = len(filtered_products)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_products = filtered_products[start:end]
    
    return jsonify({
        'success': True,
        'data': paginated_products,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    }), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    products = load_json('products.json')
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        return jsonify({'success': False, 'error': 'Product not found'}), 404
    
    return jsonify({
        'success': True,
        'data': product
    }), 200

@app.route('/api/products', methods=['POST'])
@token_required
@admin_required
def create_product(user_data):
    """Create a new product (Admin only)"""
    data = request.get_json()
    
    required_fields = ['name', 'price', 'category']
    if not all(field in data for field in required_fields):
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    products = load_json('products.json')
    
    new_product = {
        'id': get_next_id(products),
        'name': data['name'],
        'description': data.get('description', ''),
        'price': float(data['price']),
        'category': data['category'],
        'stock': data.get('stock', 0),
        'image_url': data.get('image_url', ''),
        'created_at': datetime.now().isoformat()
    }
    
    products.append(new_product)
    save_json('products.json', products)
    
    return jsonify({
        'success': True,
        'message': 'Product created successfully',
        'data': new_product
    }), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
@token_required
@admin_required
def update_product(user_data, product_id):
    """Update product (Admin only)"""
    data = request.get_json()
    products = load_json('products.json')
    
    product_index = next((i for i, p in enumerate(products) if p['id'] == product_id), None)
    
    if product_index is None:
        return jsonify({'success': False, 'error': 'Product not found'}), 404
    
    # Update allowed fields
    allowed_fields = ['name', 'description', 'price', 'category', 'stock', 'image_url']
    for field in allowed_fields:
        if field in data:
            products[product_index][field] = data[field]
    
    products[product_index]['updated_at'] = datetime.now().isoformat()
    save_json('products.json', products)
    
    return jsonify({
        'success': True,
        'message': 'Product updated successfully',
        'data': products[product_index]
    }), 200

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_product(user_data, product_id):
    """Delete product (Admin only)"""
    products = load_json('products.json')
    
    product_index = next((i for i, p in enumerate(products) if p['id'] == product_id), None)
    
    if product_index is None:
        return jsonify({'success': False, 'error': 'Product not found'}), 404
    
    deleted_product = products.pop(product_index)
    save_json('products.json', products)
    
    return jsonify({
        'success': True,
        'message': 'Product deleted successfully',
        'data': {'id': deleted_product['id'], 'name': deleted_product['name']}
    }), 200

@app.route('/api/products/search', methods=['GET'])
def search_products():
    """Search products by query"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'success': False, 'error': 'Search query is required'}), 400
    
    products = load_json('products.json')
    
    results = [p for p in products 
               if query in p.get('name', '').lower() or 
               query in p.get('description', '').lower()]
    
    return jsonify({
        'success': True,
        'data': results,
        'count': len(results)
    }), 200

@app.route('/api/products/category/<string:category>', methods=['GET'])
def get_products_by_category(category):
    """Get products by category"""
    products = load_json('products.json')
    
    category_products = [p for p in products if p.get('category', '').lower() == category.lower()]
    
    return jsonify({
        'success': True,
        'data': category_products,
        'count': len(category_products)
    }), 200

# ============== CART MANAGEMENT ==============
@app.route('/api/cart', methods=['GET'])
@token_required
def get_cart(user_data):
    """Get user's cart"""
    carts = load_json('cart.json')
    user_cart = [item for item in carts if item['user_id'] == user_data['id']]
    
    # Get product details
    products = load_json('products.json')
    cart_with_details = []
    total = 0
    
    for item in user_cart:
        product = next((p for p in products if p['id'] == item['product_id']), None)
        if product:
            item_total = product['price'] * item['quantity']
            total += item_total
            cart_with_details.append({
                **item,
                'product': product,
                'item_total': item_total
            })
    
    # Apply price fail for API testing
    total = apply_price_fail(total, 'apitotalprice')
    
    return jsonify({
        'success': True,
        'data': cart_with_details,
        'total': total,
        'count': len(cart_with_details)
    }), 200

@app.route('/api/cart/items', methods=['POST'])
@token_required
def add_to_cart(user_data):
    """Add item to cart"""
    data = request.get_json()
    
    if not data or not data.get('product_id'):
        return jsonify({'success': False, 'error': 'Product ID is required'}), 400
    
    product_id = data['product_id']
    quantity = data.get('quantity', 1)
    
    # Validate quantity new bug
    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({'success': False, 'error': 'Invalid quantity: must be a positive integer'}), 400
    
    # Verify product exists
    products = load_json('products.json')
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        return jsonify({'success': False, 'error': 'Product not found'}), 404
    
    if product.get('stock', 0) < quantity:
        return jsonify({'success': False, 'error': 'Insufficient stock'}), 400
    
    carts = load_json('cart.json')
    
    # Check if item already in cart
    existing_item = next((item for item in carts 
                         if item['user_id'] == user_data['id'] and 
                         item['product_id'] == product_id), None)
    
    if existing_item:
        # Update quantity
        existing_item['quantity'] += quantity
        existing_item['updated_at'] = datetime.now().isoformat()
    else:
        # Add new item
        new_item = {
            'id': get_next_id(carts),
            'user_id': user_data['id'],
            'product_id': product_id,
            'quantity': quantity,
            'created_at': datetime.now().isoformat()
        }
        carts.append(new_item)
    
    save_json('cart.json', carts)
    
    return jsonify({
        'success': True,
        'message': 'Item added to cart successfully'
    }), 201

@app.route('/api/cart/items/<int:item_id>', methods=['PUT'])
@token_required
def update_cart_item(user_data, item_id):
    """Update cart item quantity"""
    data = request.get_json()
    
    if 'quantity' not in data:
        return jsonify({'success': False, 'error': 'Quantity is required'}), 400
    
    carts = load_json('cart.json')
    
    item_index = next((i for i, item in enumerate(carts) 
                      if item['id'] == item_id and item['user_id'] == user_data['id']), None)
    
    if item_index is None:
        return jsonify({'success': False, 'error': 'Cart item not found'}), 404
    
    carts[item_index]['quantity'] = data['quantity']
    carts[item_index]['updated_at'] = datetime.now().isoformat()
    
    save_json('cart.json', carts)
    
    return jsonify({
        'success': True,
        'message': 'Cart item updated successfully',
        'data': carts[item_index]
    }), 200

@app.route('/api/cart/items/<int:item_id>', methods=['DELETE'])
@token_required
def remove_from_cart(user_data, item_id):
    """Remove item from cart"""
    carts = load_json('cart.json')
    
    item_index = next((i for i, item in enumerate(carts) 
                      if item['id'] == item_id and item['user_id'] == user_data['id']), None)
    
    if item_index is None:
        return jsonify({'success': False, 'error': 'Cart item not found'}), 404
    
    removed_item = carts.pop(item_index)
    save_json('cart.json', carts)
    
    return jsonify({
        'success': True,
        'message': 'Item removed from cart successfully',
        'data': removed_item
    }), 200

@app.route('/api/cart', methods=['DELETE'])
@token_required
def clear_cart(user_data):
    """Clear entire cart"""
    carts = load_json('cart.json')
    
    # Remove all items for this user
    updated_carts = [item for item in carts if item['user_id'] != user_data['id']]
    
    save_json('cart.json', updated_carts)
    
    return jsonify({
        'success': True,
        'message': 'Cart cleared successfully'
    }), 200

# ============== ORDER MANAGEMENT ==============
@app.route('/api/orders', methods=['POST'])
@token_required
def create_order(user_data):
    """Create new order from cart"""
    data = request.get_json()
    
    # Validate shipping address
    if not data or not data.get('shipping_address') or not str(data.get('shipping_address')).strip():
        return jsonify({'success': False, 'error': 'Shipping address is required'}), 400
    
    # Get user's cart
    carts = load_json('cart.json')
    user_cart = [item for item in carts if item['user_id'] == user_data['id']]
    
    if not user_cart:
        return jsonify({'success': False, 'error': 'Cart is empty'}), 400
    
    # Get product details and calculate total
    products = load_json('products.json')
    order_items = []
    total_amount = 0
    
    for cart_item in user_cart:
        product = next((p for p in products if p['id'] == cart_item['product_id']), None)
        if product:
            if product.get('stock', 0) < cart_item['quantity']:
                return jsonify({
                    'success': False, 
                    'error': f'Insufficient stock for {product["name"]}'
                }), 400
            
            item_total = product['price'] * cart_item['quantity']
            total_amount += item_total
            
            order_items.append({
                'product_id': product['id'],
                'product_name': product['name'],
                'quantity': cart_item['quantity'],
                'price': product['price'],
                'subtotal': item_total
            })
    
    # Apply price fail for API testing
    total_amount = apply_price_fail(total_amount, 'apitotalprice')
    
    # Create order
    orders = load_json('orders.json')
    
    new_order = {
        'id': get_next_id(orders),
        'user_id': user_data['id'],
        'items': order_items,
        'total_amount': total_amount,
        'status': 'pending',
        'shipping_address': data.get('shipping_address'),
        'created_at': datetime.now().isoformat()
    }
    
    orders.append(new_order)
    save_json('orders.json', orders)
    
    # Update product stock
    for item in order_items:
        product_index = next((i for i, p in enumerate(products) if p['id'] == item['product_id']), None)
        if product_index is not None:
            products[product_index]['stock'] -= item['quantity']
    save_json('products.json', products)
    
    # Clear user's cart
    updated_carts = [item for item in carts if item['user_id'] != user_data['id']]
    save_json('cart.json', updated_carts)
    
    return jsonify({
        'success': True,
        'message': 'Order created successfully',
        'data': new_order
    }), 201

@app.route('/api/orders', methods=['GET'])
@token_required
def get_orders(user_data):
    """Get user's orders"""
    orders = load_json('orders.json')
    
    if user_data.get('is_admin', False):
        # Admin can see all orders
        user_orders = orders
    else:
        # Regular users see only their orders
        user_orders = [o for o in orders if o['user_id'] == user_data['id']]
    
    return jsonify({
        'success': True,
        'data': user_orders,
        'count': len(user_orders)
    }), 200

@app.route('/api/orders/<int:order_id>', methods=['GET'])
@token_required
def get_order(user_data, order_id):
    """Get order by ID"""
    orders = load_json('orders.json')
    order = next((o for o in orders if o['id'] == order_id), None)
    
    if not order:
        return jsonify({'success': False, 'error': 'Order not found'}), 404
    
    # Check authorization
    if order['user_id'] != user_data['id'] and not user_data.get('is_admin', False):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    return jsonify({
        'success': True,
        'data': order
    }), 200

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
@token_required
@admin_required
def update_order_status(user_data, order_id):
    """Update order status (Admin only) with workflow validation"""
    data = request.get_json()
    
    if 'status' not in data:
        return jsonify({'success': False, 'error': 'Status is required'}), 400
    
    valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    if data['status'] not in valid_statuses:
        return jsonify({'success': False, 'error': 'Invalid status'}), 400
    
    orders = load_json('orders.json')
    
    order_index = next((i for i, o in enumerate(orders) if o['id'] == order_id), None)
    
    if order_index is None:
        return jsonify({'success': False, 'error': 'Order not found'}), 404
    
    current_status = orders[order_index]['status']
    new_status = data['status']
    
    # WORKFLOW VALIDATION: Define allowed status transitions
    allowed_transitions = {
        'pending': ['processing', 'cancelled'],
        'processing': ['shipped', 'cancelled'],
        'shipped': ['delivered', 'cancelled'],
        'delivered': [],  # Terminal state
        'cancelled': []   # Terminal state
    }
    
    # Allow staying in same status (idempotent)
    if current_status == new_status:
        return jsonify({
            'success': True,
            'message': 'Order status unchanged',
            'data': orders[order_index]
        }), 200
    
    # Validate transition
    if new_status not in allowed_transitions.get(current_status, []):
        return jsonify({
            'success': False, 
            'error': f'Cannot transition from {current_status} to {new_status}. Allowed: {", ".join(allowed_transitions.get(current_status, ["none"]))}'
        }), 400
    
    orders[order_index]['status'] = new_status
    orders[order_index]['updated_at'] = datetime.now().isoformat()
    
    save_json('orders.json', orders)
    
    return jsonify({
        'success': True,
        'message': 'Order status updated successfully',
        'data': orders[order_index]
    }), 200

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
@token_required
def update_order(user_data, order_id):
    """Update order details"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Request data is required'}), 400
    
    orders = load_json('orders.json')
    
    order_index = next((i for i, o in enumerate(orders) if o['id'] == order_id), None)
    
    if order_index is None:
        return jsonify({'success': False, 'error': 'Order not found'}), 404
    
    order = orders[order_index]
    
    # Check authorization
    if order['user_id'] != user_data['id'] and not user_data.get('is_admin', False):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    # Can only update pending or processing orders
    if order['status'] not in ['pending', 'processing']:
        return jsonify({'success': False, 'error': 'Cannot update this order'}), 400
    
    # Update allowed fields
    allowed_fields = ['shipping_address']
    for field in allowed_fields:
        if field in data:
            orders[order_index][field] = data[field]
    
    orders[order_index]['updated_at'] = datetime.now().isoformat()
    save_json('orders.json', orders)
    
    return jsonify({
        'success': True,
        'message': 'Order updated successfully',
        'data': orders[order_index]
    }), 200

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
@token_required
def cancel_order(user_data, order_id):
    """Cancel order and restore items to cart"""
    orders = load_json('orders.json')
    
    order_index = next((i for i, o in enumerate(orders) if o['id'] == order_id), None)
    
    if order_index is None:
        return jsonify({'success': False, 'error': 'Order not found'}), 404
    
    order = orders[order_index]
    
    # Check authorization
    if order['user_id'] != user_data['id'] and not user_data.get('is_admin', False):
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    # Determine allowed cancel statuses based on role
    if user_data.get('is_admin', False):
        allowed_cancel_statuses = ['pending', 'processing']
    else:
        # Regular users can only cancel pending orders
        allowed_cancel_statuses = ['pending']

    if order['status'] not in allowed_cancel_statuses:
        return jsonify({'success': False, 'error': f'Cannot cancel this order. Allowed statuses: {", ".join(allowed_cancel_statuses)}'}), 400
    
    # Restore stock
    products = load_json('products.json')
    for item in order['items']:
        product_index = next((i for i, p in enumerate(products) if p['id'] == item['product_id']), None)
        if product_index is not None:
            products[product_index]['stock'] += item['quantity']
    save_json('products.json', products)
    
    # FEATURE: Restore items to cart
    carts = load_json('cart.json')
    for item in order['items']:
        # Check if product still exists
        product = next((p for p in products if p['id'] == item['product_id']), None)
        if product:
            # Check if item already in cart
            existing_cart_item = next((c for c in carts 
                                     if c['user_id'] == user_data['id'] and 
                                     c['product_id'] == item['product_id']), None)
            
            if existing_cart_item:
                # Increase quantity
                existing_cart_item['quantity'] += item['quantity']
                existing_cart_item['updated_at'] = datetime.now().isoformat()
            else:
                # Add new cart item
                new_cart_item = {
                    'id': get_next_id(carts),
                    'user_id': user_data['id'],
                    'product_id': item['product_id'],
                    'quantity': item['quantity'],
                    'created_at': datetime.now().isoformat()
                }
                carts.append(new_cart_item)
    
    save_json('cart.json', carts)
    
    # Update order status
    orders[order_index]['status'] = 'cancelled'
    orders[order_index]['cancelled_at'] = datetime.now().isoformat()
    orders[order_index]['cart_restored'] = True
    
    save_json('orders.json', orders)
    
    return jsonify({
        'success': True,
        'message': 'Order cancelled successfully. Items restored to cart.',
        'data': orders[order_index],
        'items_restored': len(order['items'])
    }), 200

@app.route('/api/orders/status/<string:status>', methods=['GET'])
@token_required
def get_orders_by_status(user_data, status):
    """Get orders by status"""
    orders = load_json('orders.json')
    
    if user_data.get('is_admin', False):
        filtered_orders = [o for o in orders if o['status'] == status]
    else:
        filtered_orders = [o for o in orders 
                          if o['user_id'] == user_data['id'] and o['status'] == status]
    
    return jsonify({
        'success': True,
        'data': filtered_orders,
        'count': len(filtered_orders)
    }), 200

# ============== CATEGORIES ==============
@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = load_json('categories.json')
    
    return jsonify({
        'success': True,
        'data': categories,
        'count': len(categories)
    }), 200

@app.route('/api/categories', methods=['POST'])
@token_required
@admin_required
def create_category(user_data):
    """Create new category (Admin only)"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'success': False, 'error': 'Category name is required'}), 400
    
    categories = load_json('categories.json')
    
    new_category = {
        'id': get_next_id(categories),
        'name': data['name'],
        'description': data.get('description', ''),
        'created_at': datetime.now().isoformat()
    }
    
    categories.append(new_category)
    save_json('categories.json', categories)
    
    return jsonify({
        'success': True,
        'message': 'Category created successfully',
        'data': new_category
    }), 201

@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_category(user_data, category_id):
    """Delete category (Admin only)"""
    categories = load_json('categories.json')

    category_index = next((i for i, c in enumerate(categories) if c['id'] == category_id), None)

    if category_index is None:
        return jsonify({'success': False, 'error': 'Category not found'}), 404

    # VALIDATION: Check if category has products
    products = load_json('products.json')
    category_name = categories[category_index]['name']
    products_in_category = [p for p in products if p.get('category') == category_name]
    
    if products_in_category:
        return jsonify({
            'success': False, 
            'error': f'Cannot delete category with {len(products_in_category)} products. Remove products first.'
        }), 400

    deleted_category = categories.pop(category_index)
    save_json('categories.json', categories)

    return jsonify({
        'success': True,
        'message': 'Category deleted successfully',
        'data': {'id': deleted_category['id'], 'name': deleted_category['name']}
    }), 200

# ============== LIKES ==============
@app.route('/api/products/likes', methods=['POST'])
@token_required
def toggle_product_like(user_data):
    """Like/unlike a product (users can only like once)"""
    data = request.get_json()
    
    if not data or not data.get('product_id'):
        return jsonify({'success': False, 'error': 'Product ID is required'}), 400
    
    # Verify product exists
    products = load_json('products.json')
    if not any(p['id'] == data['product_id'] for p in products):
        return jsonify({'success': False, 'error': 'Product not found'}), 404
    
    # Load likes data
    likes = load_json('likes.json')
    
    # Check if user already liked this product (prevent duplicates)
    existing_like = next((l for l in likes if l['user_id'] == user_data['id'] and l['product_id'] == data['product_id']), None)
    
    if existing_like:
        return jsonify({
            'success': False, 
            'error': 'You have already liked this product',
            'already_liked': True
        }), 400
    
    # Add new like
    new_like = {
        'id': get_next_id(likes),
        'user_id': user_data['id'],
        'product_id': data['product_id'],
        'created_at': datetime.now().isoformat()
    }
    
    likes.append(new_like)
    save_json('likes.json', likes)
    
    return jsonify({
        'success': True,
        'message': 'Product liked successfully',
        'data': new_like
    }), 201

@app.route('/api/products/<int:product_id>/likes', methods=['GET'])
def get_product_likes(product_id):
    """Get likes count for a product"""
    likes = load_json('likes.json')
    product_likes = [l for l in likes if l['product_id'] == product_id]
    
    return jsonify({
        'success': True,
        'data': product_likes,
        'count': len(product_likes)
    }), 200

@app.route('/api/products/<int:product_id>/likes/check', methods=['GET'])
@token_required
def check_user_like(user_data, product_id):
    """Check if current user has liked a product"""
    likes = load_json('likes.json')
    user_like = next((l for l in likes if l['user_id'] == user_data['id'] and l['product_id'] == product_id), None)
    
    return jsonify({
        'success': True,
        'liked': user_like is not None,
        'data': user_like
    }), 200

@app.route('/api/products/likes/<int:like_id>', methods=['DELETE'])
@token_required
def unlike_product(user_data, like_id):
    """Unlike a product (remove like)"""
    likes = load_json('likes.json')
    
    like_index = next((i for i, l in enumerate(likes) if l['id'] == like_id), None)
    
    if like_index is None:
        return jsonify({'success': False, 'error': 'Like not found'}), 404
    
    # Verify the like belongs to the authenticated user
    if likes[like_index]['user_id'] != user_data['id']:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    removed_like = likes.pop(like_index)
    save_json('likes.json', likes)
    
    return jsonify({
        'success': True,
        'message': 'Product unliked successfully',
        'data': removed_like
    }), 200

@app.route('/api/likes/cleanup', methods=['POST'])
@token_required
@admin_required
def cleanup_duplicate_likes(user_data):
    """Remove duplicate likes (Admin only)"""
    likes = load_json('likes.json')
    
    # Find and remove duplicates
    seen = set()
    unique_likes = []
    duplicates_removed = 0
    
    for like in likes:
        key = (like['user_id'], like['product_id'])
        if key not in seen:
            seen.add(key)
            unique_likes.append(like)
        else:
            duplicates_removed += 1
    
    save_json('likes.json', unique_likes)
    
    return jsonify({
        'success': True,
        'message': f'Removed {duplicates_removed} duplicate likes',
        'duplicates_removed': duplicates_removed,
        'remaining_likes': len(unique_likes)
    }), 200

# ============== REVIEWS ==============
@app.route('/api/reviews', methods=['POST'])
@token_required
def create_review(user_data):
    """Create product review"""
    data = request.get_json()
    
    if not data or not data.get('product_id') or not data.get('rating'):
        return jsonify({'success': False, 'error': 'Product ID and rating are required'}), 400
    
    if not 1 <= data['rating'] <= 5:
        return jsonify({'success': False, 'error': 'Rating must be between 1 and 5'}), 400
    
    # Verify product exists
    products = load_json('products.json')
    if not any(p['id'] == data['product_id'] for p in products):
        return jsonify({'success': False, 'error': 'Product not found'}), 404
    
    reviews = load_json('reviews.json')
    
    # Check if user has already reviewed this product
    existing_review = next((r for r in reviews if r['user_id'] == user_data['id'] and r['product_id'] == data['product_id']), None)
    if existing_review:
        return jsonify({'success': False, 'error': 'You have already reviewed this product'}), 400
    
    new_review = {
        'id': get_next_id(reviews),
        'user_id': user_data['id'],
        'product_id': data['product_id'],
        'rating': data['rating'],
        'comment': data.get('comment', ''),
        'created_at': datetime.now().isoformat()
    }
    
    reviews.append(new_review)
    save_json('reviews.json', reviews)
    
    return jsonify({
        'success': True,
        'message': 'Review created successfully',
        'data': new_review
    }), 201

@app.route('/api/products/<int:product_id>/reviews/check', methods=['GET'])
@token_required
def check_user_review(user_data, product_id):
    """Check if user has already reviewed this product"""
    reviews = load_json('reviews.json')
    
    existing_review = next((r for r in reviews if r['user_id'] == user_data['id'] and r['product_id'] == product_id), None)
    
    return jsonify({
        'success': True,
        'has_reviewed': existing_review is not None,
        'review': existing_review if existing_review else None
    }), 200

@app.route('/api/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    """Get reviews for a product"""
    reviews = load_json('reviews.json')
    product_reviews = [r for r in reviews if r['product_id'] == product_id]
    
    # Calculate average rating
    if product_reviews:
        avg_rating = sum(r['rating'] for r in product_reviews) / len(product_reviews)
    else:
        avg_rating = 0
    
    return jsonify({
        'success': True,
        'data': product_reviews,
        'count': len(product_reviews),
        'average_rating': round(avg_rating, 2)
    }), 200

# ============== STATISTICS (ADMIN) ==============
@app.route('/api/stats', methods=['GET'])
@token_required
@admin_required
def get_stats(user_data):
    """Get dashboard statistics (Admin only)"""
    users = load_json('users.json')
    products = load_json('products.json')
    orders = load_json('orders.json')
    reviews = load_json('reviews.json')
    
    # Calculate statistics
    total_users = len(users)
    total_products = len(products)
    total_orders = len(orders)
    total_revenue = sum(o['total_amount'] for o in orders if o['status'] != 'cancelled')
    
    pending_orders = len([o for o in orders if o['status'] == 'pending'])
    low_stock_products = len([p for p in products if p.get('stock', 0) < 10])
    
    return jsonify({
        'success': True,
        'data': {
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_revenue': round(total_revenue, 2),
            'pending_orders': pending_orders,
            'low_stock_products': low_stock_products,
            'total_reviews': len(reviews)
        }
    }), 200

# ============== INVENTORY MANAGEMENT ==============
@app.route('/api/inventory/low-stock', methods=['GET'])
@token_required
@admin_required
def get_low_stock_products(user_data):
    """Get products with low stock (Admin only)"""
    products = load_json('products.json')
    threshold = request.args.get('threshold', 10, type=int)
    
    low_stock_products = [p for p in products if p.get('stock', 0) <= threshold]
    
    return jsonify({
        'success': True,
        'data': low_stock_products,
        'count': len(low_stock_products),
        'threshold': threshold
    }), 200

@app.route('/api/inventory/update-stock', methods=['PUT'])
@token_required
@admin_required
def update_product_stock(user_data):
    """Update product stock (Admin only)"""
    data = request.get_json()
    
    if not data or not data.get('product_id') or 'stock' not in data:
        return jsonify({'success': False, 'error': 'Product ID and stock are required'}), 400
    
    products = load_json('products.json')
    product_index = next((i for i, p in enumerate(products) if p['id'] == data['product_id']), None)
    
    if product_index is None:
        return jsonify({'success': False, 'error': 'Product not found'}), 404
    
    old_stock = products[product_index]['stock']
    products[product_index]['stock'] = data['stock']
    products[product_index]['updated_at'] = datetime.now().isoformat()
    
    save_json('products.json', products)
    
    return jsonify({
        'success': True,
        'message': 'Stock updated successfully',
        'data': {
            'product_id': data['product_id'],
            'old_stock': old_stock,
            'new_stock': data['stock']
        }
    }), 200

# ============== USER ACTIVITY TRACKING ==============
@app.route('/api/users/<int:user_id>/activity', methods=['GET'])
@token_required
@admin_required
def get_user_activity(user_data, user_id):
    """Get user activity (Admin only)"""
    orders = load_json('orders.json')
    reviews = load_json('reviews.json')
    carts = load_json('cart.json')
    
    user_orders = [o for o in orders if o['user_id'] == user_id]
    user_reviews = [r for r in reviews if r['user_id'] == user_id]
    user_cart_items = [c for c in carts if c['user_id'] == user_id]
    
    # Calculate total spent
    total_spent = sum(o['total_amount'] for o in user_orders if o['status'] != 'cancelled')
    
    return jsonify({
        'success': True,
        'data': {
            'user_id': user_id,
            'total_orders': len(user_orders),
            'total_reviews': len(user_reviews),
            'cart_items': len(user_cart_items),
            'total_spent': total_spent,
            'orders': user_orders,
            'reviews': user_reviews
        }
    }), 200

# ============== BULK OPERATIONS ==============
@app.route('/api/products/bulk-update', methods=['PUT'])
@token_required
@admin_required
def bulk_update_products(user_data):
    """Bulk update products (Admin only)"""
    data = request.get_json()
    
    if not data or not data.get('updates'):
        return jsonify({'success': False, 'error': 'Updates array is required'}), 400
    
    products = load_json('products.json')
    updated_count = 0
    
    for update in data['updates']:
        product_index = next((i for i, p in enumerate(products) if p['id'] == update['product_id']), None)
        if product_index is not None:
            # Update allowed fields
            allowed_fields = ['name', 'description', 'price', 'category', 'stock', 'image_url']
            for field in allowed_fields:
                if field in update:
                    products[product_index][field] = update[field]
            
            products[product_index]['updated_at'] = datetime.now().isoformat()
            updated_count += 1
    
    save_json('products.json', products)
    
    return jsonify({
        'success': True,
        'message': f'{updated_count} products updated successfully',
        'updated_count': updated_count
    }), 200

# ============== EXPORT FUNCTIONALITY ==============
@app.route('/api/export/products', methods=['GET'])
@token_required
@admin_required
def export_products(user_data):
    """Export products to JSON (Admin only)"""
    products = load_json('products.json')
    
    export_data = {
        'export_date': datetime.now().isoformat(),
        'total_products': len(products),
        'products': products
    }
    
    return jsonify({
        'success': True,
        'data': export_data
    }), 200

@app.route('/api/export/orders', methods=['GET'])
@token_required
@admin_required
def export_orders(user_data):
    """Export orders to JSON (Admin only)"""
    orders = load_json('orders.json')
    
    # Optional date filtering
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date and end_date:
        filtered_orders = [o for o in orders 
                          if start_date <= o['created_at'][:10] <= end_date]
    else:
        filtered_orders = orders
    
    export_data = {
        'export_date': datetime.now().isoformat(),
        'period': {'start_date': start_date, 'end_date': end_date},
        'total_orders': len(filtered_orders),
        'orders': filtered_orders
    }
    
    return jsonify({
        'success': True,
        'data': export_data
    }), 200

# ============== SYSTEM HEALTH & MONITORING ==============
@app.route('/api/system/health', methods=['GET'])
def system_health():
    """Get system health status"""
    try:
        # Check if all data files are accessible
        data_files = ['users.json', 'products.json', 'orders.json', 'categories.json', 
                     'reviews.json', 'cart.json', 'help.json', 'contact_messages.json',
                     'wishlist.json', 'coupons.json', 'notifications.json', 'analytics.json']
        
        file_status = {}
        for filename in data_files:
            try:
                load_json(filename)
                file_status[filename] = 'ok'
            except Exception as e:
                file_status[filename] = f'error: {str(e)}'
        
        # Get system metrics
        users = load_json('users.json')
        products = load_json('products.json')
        orders = load_json('orders.json')
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'data_files': file_status,
            'metrics': {
                'total_users': len(users),
                'total_products': len(products),
                'total_orders': len(orders)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# ============== API DOCUMENTATION ==============
@app.route('/api/docs', methods=['GET'])
def api_documentation():
    """Get API documentation"""
    endpoints = {
        'authentication': {
            'POST /api/register': 'Register a new user',
            'POST /api/login': 'User login',
        },
        'users': {
            'GET /api/users': 'Get all users (Admin)',
            'GET /api/users/{id}': 'Get user by ID',
            'PUT /api/users/{id}': 'Update user information',
            'DELETE /api/users/{id}': 'Delete user (Admin)',
        },
        'products': {
            'GET /api/products': 'Get all products with filtering',
            'GET /api/products/{id}': 'Get product by ID',
            'POST /api/products': 'Create product (Admin)',
            'PUT /api/products/{id}': 'Update product (Admin)',
            'DELETE /api/products/{id}': 'Delete product (Admin)',
            'GET /api/products/search': 'Search products',
            'GET /api/products/category/{category}': 'Get products by category',
        },
        'cart': {
            'GET /api/cart': 'Get user cart',
            'POST /api/cart/items': 'Add item to cart',
            'PUT /api/cart/items/{id}': 'Update cart item',
            'DELETE /api/cart/items/{id}': 'Remove from cart',
            'DELETE /api/cart': 'Clear cart',
        },
        'orders': {
            'POST /api/orders': 'Create order',
            'GET /api/orders': 'Get user orders',
            'GET /api/orders/{id}': 'Get order by ID',
            'PUT /api/orders/{id}': 'Update order details (shipping address)',
            'PUT /api/orders/{id}/status': 'Update order status (Admin)',
            'DELETE /api/orders/{id}': 'Cancel order',
            'GET /api/orders/status/{status}': 'Get orders by status',
        },
        'reviews': {
            'POST /api/reviews': 'Create product review',
            'GET /api/products/{id}/reviews': 'Get product reviews',
        },
        'help': {
            'GET /api/help': 'Get help articles',
            'GET /api/help/categories': 'Get help categories',
            'GET /api/help/{id}': 'Get help article',
            'POST /api/help/{id}/helpful': 'Mark article helpful',
            'POST /api/help': 'Create help article (Admin)',
            'PUT /api/help/{id}': 'Update help article (Admin)',
        },
        'contact': {
            'POST /api/contact': 'Submit contact message',
            'GET /api/contact/messages': 'Get contact messages (Admin)',
            'POST /api/contact/messages/{id}/respond': 'Respond to message (Admin)',
        },
        'wishlist': {
            'GET /api/wishlist': 'Get user wishlist',
            'POST /api/wishlist': 'Add to wishlist',
            'DELETE /api/wishlist/{id}': 'Remove from wishlist',
        },
        'coupons': {
            'GET /api/coupons': 'Get available coupons',
            'POST /api/coupons/validate': 'Validate coupon code',
            'POST /api/coupons': 'Create coupon (Admin)',
        },
        'notifications': {
            'GET /api/notifications': 'Get user notifications',
            'PUT /api/notifications/{id}/read': 'Mark notification as read',
            'PUT /api/notifications/read-all': 'Mark all notifications as read',
        },
        'analytics': {
            'GET /api/analytics/dashboard': 'Get dashboard analytics (Admin)',
            'GET /api/analytics/reports/sales': 'Get sales report (Admin)',
        },
        'search': {
            'GET /api/search/advanced': 'Advanced product search',
        },
        'recommendations': {
            'GET /api/recommendations/{id}': 'Get product recommendations',
            'GET /api/recommendations/user/{id}': 'Get user recommendations',
        },
        'blog': {
            'GET /api/blog/posts': 'Get blog posts',
            'GET /api/blog/posts/{id}': 'Get blog post',
        },
        'admin': {
            'GET /api/stats': 'Get dashboard statistics',
            'GET /api/inventory/low-stock': 'Get low stock products',
            'PUT /api/inventory/update-stock': 'Update product stock',
            'GET /api/users/{id}/activity': 'Get user activity',
            'PUT /api/products/bulk-update': 'Bulk update products',
            'GET /api/export/products': 'Export products',
            'GET /api/export/orders': 'Export orders',
        },
        'system': {
            'GET /api/health': 'Health check',
            'GET /api/system/health': 'System health status',
            'GET /api/docs': 'API documentation',
        }
    }
    
    return jsonify({
        'success': True,
        'title': 'E-Commerce API Documentation',
        'version': '2.0',
        'description': 'Comprehensive e-commerce API with advanced features',
        'base_url': request.base_url.replace('/api/docs', '/api'),
        'total_endpoints': sum(len(category) for category in endpoints.values()),
        'endpoints': endpoints,
        'features': [
            'User Authentication & Management',
            'Product Catalog & Inventory',
            'Shopping Cart & Orders',
            'Reviews & Ratings',
            'Help & FAQ System',
            'Contact Management',
            'Wishlist Functionality',
            'Coupon & Discount System',
            'Notification System',
            'Analytics & Reporting',
            'Advanced Search',
            'Product Recommendations',
            'Blog & Content Management',
            'Admin Dashboard',
            'Bulk Operations',
            'Data Export',
            'System Monitoring'
        ]
    }), 200




# ============== TESTING FRAMEWORK ==============
@app.route('/data/fail.json')
def get_fail_config():
    """Serve testing configuration file"""
    try:
        with open(os.path.join(Config.DATA_DIR, 'fail.json'), 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'error': 'fail.json not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============== WEB UI ROUTES ==============

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/web/login')
def login_page():
    """Login page"""
    return render_template('login.html')

@app.route('/web/register')
def register_page():
    """Register page"""
    return render_template('register.html')

@app.route('/web/products')
def products_page():
    """Products listing page"""
    return render_template('products.html')

@app.route('/web/products/<int:product_id>')
def product_detail_page(product_id):
    """Product detail page"""
    return render_template('product_detail.html', product_id=product_id)

@app.route('/web/cart')
def cart_page():
    """Shopping cart page"""
    return render_template('cart.html')

@app.route('/web/orders')
def orders_page():
    """Orders page"""
    return render_template('orders.html')

@app.route('/web/profile')
def profile_page():
    """User profile page"""
    return render_template('profile.html')

@app.route('/web/admin')
def admin_page():
    """Admin dashboard page"""
    return render_template('admin.html')

@app.route('/web/test-framework')
def test_framework_page():
    """Testing framework demo page"""
    return render_template('test_framework.html')

@app.route('/web/help')
def help_page():
    """Help and FAQ page"""
    return render_template('help.html')

@app.route('/web/contact')
def contact_page():
    """Contact page"""
    return render_template('contact.html')

@app.route('/web/wishlist')
def wishlist_page():
    """Wishlist page"""
    return render_template('wishlist.html')

@app.route('/web/notifications')
def notifications_page():
    """Notifications page"""
    return render_template('notifications.html')

@app.route('/web/blog')
def blog_page():
    """Blog page"""
    return render_template('blog.html')

@app.route('/web/advanced-search')
def advanced_search_page():
    """Advanced search page"""
    return render_template('advanced_search.html')



# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
