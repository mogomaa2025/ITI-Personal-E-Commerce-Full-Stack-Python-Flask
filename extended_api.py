#!/usr/bin/env python3
"""
Extended API endpoints for graduation project
This file contains advanced features and endpoints
"""

from flask import Flask, jsonify, request
from functools import wraps
import json
import os
from datetime import datetime, timedelta
import random
from auth import generate_token, verify_token, hash_password, verify_password
from utils import load_json, save_json, get_next_id, validate_email

# Import decorators from app.py
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

def admin_required(f):
    @wraps(f)
    def decorated(user_data, *args, **kwargs):
        if not user_data.get('is_admin', False):
            return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
        return f(user_data, *args, **kwargs)
    return decorated

# ============== HELP & FAQ SYSTEM ==============

def help_routes(app):
    """Help and FAQ system routes"""
    
    @app.route('/api/help', methods=['GET'])
    def get_help_articles():
        """Get all help articles with optional filtering"""
        help_data = load_json('help.json')
        
        category = request.args.get('category')
        search = request.args.get('search', '').lower()
        
        filtered_articles = help_data
        
        if category:
            filtered_articles = [h for h in filtered_articles if h.get('category', '').lower() == category.lower()]
        
        if search:
            filtered_articles = [h for h in filtered_articles 
                               if search in h.get('question', '').lower() or 
                               search in h.get('answer', '').lower()]
        
        # Sort by helpful count
        filtered_articles.sort(key=lambda x: x.get('helpful_count', 0), reverse=True)
        
        return jsonify({
            'success': True,
            'data': filtered_articles,
            'count': len(filtered_articles)
        }), 200
    
    @app.route('/api/help/categories', methods=['GET'])
    def get_help_categories():
        """Get all help categories"""
        help_data = load_json('help.json')
        categories = list(set(h.get('category', '') for h in help_data))
        
        return jsonify({
            'success': True,
            'data': categories
        }), 200
    
    @app.route('/api/help/<int:help_id>', methods=['GET'])
    def get_help_article(help_id):
        """Get specific help article"""
        help_data = load_json('help.json')
        article = next((h for h in help_data if h['id'] == help_id), None)
        
        if not article:
            return jsonify({'success': False, 'error': 'Article not found'}), 404
        
        return jsonify({
            'success': True,
            'data': article
        }), 200
    

    @app.route('/api/help/<int:help_id>/helpful', methods=['POST'])
    def mark_helpful(help_id):
        """Mark help article as helpful (one-time per user)"""
        help_data = load_json('help.json')
        
        article_index = next((i for i, h in enumerate(help_data) if h['id'] == help_id), None)
        
        if article_index is None:
            return jsonify({'success': False, 'error': 'Article not found'}), 404
        
        # Load helpful votes data
        helpful_votes = load_json('helpful_votes.json')
        
        # Get user identifier (IP address as fallback for anonymous users)
        user_identifier = request.remote_addr
        if request.headers.get('Authorization'):
            try:
                from auth import verify_token
                token = request.headers.get('Authorization').replace('Bearer ', '')
                user_data = verify_token(token)
                if user_data:
                    user_identifier = f"user_{user_data['id']}"
            except:
                pass  # Use IP as fallback
        
        # Check if user already voted for this article
        existing_vote = next((v for v in helpful_votes 
                           if v['user_identifier'] == user_identifier and v['help_id'] == help_id), None)
        
        if existing_vote:
            return jsonify({
                'success': False, 
                'error': 'You have already marked this article as helpful',
                'already_helpful': True
            }), 400
        
        # Add new vote
        new_vote = {
            'id': get_next_id(helpful_votes),
            'help_id': help_id,
            'user_identifier': user_identifier,
            'created_at': datetime.now().isoformat()
        }
        
        helpful_votes.append(new_vote)
        save_json('helpful_votes.json', helpful_votes)
        
        # Update helpful count
        help_data[article_index]['helpful_count'] = help_data[article_index].get('helpful_count', 0) + 1
        save_json('help.json', help_data)
        
        return jsonify({
            'success': True,
            'message': 'Thank you for your feedback!'
        }), 200
    
    @app.route('/api/help', methods=['POST'])
    @app.route('/api/help/<int:help_id>', methods=['PUT'])
    @token_required
    @admin_required
    def manage_help_article(user_data, help_id=None):
        """Create or update help article (Admin only)"""
        data = request.get_json()
        
        if not data or not data.get('question') or not data.get('answer'):
            return jsonify({'success': False, 'error': 'Question and answer are required'}), 400
        
        help_data = load_json('help.json')
        
        if help_id:
            # Update existing article
            article_index = next((i for i, h in enumerate(help_data) if h['id'] == help_id), None)
            if article_index is None:
                return jsonify({'success': False, 'error': 'Article not found'}), 404
            
            help_data[article_index].update({
                'question': data['question'],
                'answer': data['answer'],
                'category': data.get('category', 'General'),
                'updated_at': datetime.now().isoformat()
            })
            message = 'Article updated successfully'
        else:
            # Create new article
            new_article = {
                'id': get_next_id(help_data),
                'question': data['question'],
                'answer': data['answer'],
                'category': data.get('category', 'General'),
                'helpful_count': 0,
                'created_at': datetime.now().isoformat()
            }
            help_data.append(new_article)
            message = 'Article created successfully'
        
        save_json('help.json', help_data)
        
        return jsonify({
            'success': True,
            'message': message
        }), 200

# ============== CONTACT SYSTEM ==============

def contact_routes(app):
    """Contact system routes"""
    
    @app.route('/api/contact', methods=['POST'])
    def submit_contact_message():
        """Submit contact message"""
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({'success': False, 'error': 'Name, email, and message are required'}), 400
        
        if not validate_email(data['email']):
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400
        
        contact_messages = load_json('contact_messages.json')
        
        new_message = {
            'id': get_next_id(contact_messages),
            'name': data['name'],
            'email': data['email'],
            'subject': data.get('subject', 'General Inquiry'),
            'message': data['message'],
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        
        contact_messages.append(new_message)
        save_json('contact_messages.json', contact_messages)
        
        return jsonify({
            'success': True,
            'message': 'Your message has been submitted successfully. We will get back to you soon!'
        }), 201
    
    @app.route('/api/contact/messages', methods=['GET'])
    @token_required
    @admin_required
    def get_contact_messages(user_data):
        """Get contact messages (Admin only)"""
        contact_messages = load_json('contact_messages.json')
        
        status = request.args.get('status')
        if status:
            contact_messages = [m for m in contact_messages if m.get('status') == status]
        
        return jsonify({
            'success': True,
            'data': contact_messages,
            'count': len(contact_messages)
        }), 200
    
    @app.route('/api/contact/messages/<int:message_id>/respond', methods=['POST'])
    @token_required
    @admin_required
    def respond_to_contact_message(user_data, message_id):
        """Respond to contact message (Admin only)"""
        data = request.get_json()
        
        if not data or not data.get('response'):
            return jsonify({'success': False, 'error': 'Response is required'}), 400
        
        contact_messages = load_json('contact_messages.json')
        
        message_index = next((i for i, m in enumerate(contact_messages) if m['id'] == message_id), None)
        
        if message_index is None:
            return jsonify({'success': False, 'error': 'Message not found'}), 404
        
        contact_messages[message_index].update({
            'response': data['response'],
            'status': 'resolved',
            'resolved_at': datetime.now().isoformat()
        })
        
        save_json('contact_messages.json', contact_messages)
        
        return jsonify({
            'success': True,
            'message': 'Response sent successfully'
        }), 200

# ============== WISHLIST SYSTEM ==============

def wishlist_routes(app):
    """Wishlist system routes"""
    
    @app.route('/api/wishlist', methods=['GET'])
    @token_required
    def get_wishlist(user_data):
        """Get user's wishlist"""
        user_id = user_data['id']
        
        wishlist_data = load_json('wishlist.json')
        user_wishlist = [w for w in wishlist_data if w['user_id'] == user_id]
        
        # Get product details
        products = load_json('products.json')
        wishlist_with_details = []
        
        for item in user_wishlist:
            product = next((p for p in products if p['id'] == item['product_id']), None)
            if product:
                wishlist_with_details.append({
                    **item,
                    'product': product
                })
        
        return jsonify({
            'success': True,
            'data': wishlist_with_details,
            'count': len(wishlist_with_details)
        }), 200
    
    @app.route('/api/wishlist', methods=['POST'])
    @token_required
    def add_to_wishlist(user_data):
        """Add product to wishlist"""
        data = request.get_json()
        
        if not data or not data.get('product_id'):
            return jsonify({'success': False, 'error': 'Product ID is required'}), 400
        
        user_id = user_data['id']
        
        # Verify product exists
        products = load_json('products.json')
        if not any(p['id'] == data['product_id'] for p in products):
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        wishlist_data = load_json('wishlist.json')
        
        # Check if already in wishlist
        if any(w['user_id'] == user_id and w['product_id'] == data['product_id'] for w in wishlist_data):
            return jsonify({'success': False, 'error': 'Product already in wishlist'}), 400
        
        new_item = {
            'id': get_next_id(wishlist_data),
            'user_id': user_id,
            'product_id': data['product_id'],
            'created_at': datetime.now().isoformat()
        }
        
        wishlist_data.append(new_item)
        save_json('wishlist.json', wishlist_data)
        
        return jsonify({
            'success': True,
            'message': 'Product added to wishlist successfully'
        }), 201
    
    @app.route('/api/wishlist/<int:item_id>', methods=['DELETE'])
    @token_required
    def remove_from_wishlist(user_data, item_id):
        """Remove product from wishlist"""
        wishlist_data = load_json('wishlist.json')
        
        item_index = next((i for i, w in enumerate(wishlist_data) if w['id'] == item_id), None)
        
        if item_index is None:
            return jsonify({'success': False, 'error': 'Wishlist item not found'}), 404
        
        # Verify the item belongs to the authenticated user
        if wishlist_data[item_index]['user_id'] != user_data['id']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        removed_item = wishlist_data.pop(item_index)
        save_json('wishlist.json', wishlist_data)
        
        return jsonify({
            'success': True,
            'message': 'Product removed from wishlist successfully'
        }), 200

# ============== COUPON SYSTEM ==============

def coupon_routes(app):
    """Coupon and discount system routes"""
    
    @app.route('/api/coupons', methods=['GET'])
    @token_required
    @admin_required
    def get_coupons(user_data):
        """Get available coupons (Admin only)"""
        coupons = load_json('coupons.json')
        
        # Filter active coupons
        active_coupons = [c for c in coupons if c.get('is_active', True)]
        
        # Filter by expiration
        current_time = datetime.now()
        valid_coupons = []
        
        for coupon in active_coupons:
            expires_at = datetime.fromisoformat(coupon['expires_at'].replace('Z', '+00:00'))
            if expires_at > current_time:
                valid_coupons.append(coupon)
        
        return jsonify({
            'success': True,
            'data': valid_coupons,
            'count': len(valid_coupons)
        }), 200
    
    @app.route('/api/coupons/validate', methods=['POST'])
    @token_required
    def validate_coupon(user_data):
        """Validate coupon code"""
        data = request.get_json()
        
        if not data or not data.get('code') or not data.get('order_amount'):
            return jsonify({'success': False, 'error': 'Coupon code and order amount are required'}), 400
        
        coupons = load_json('coupons.json')
        coupon = next((c for c in coupons if c['code'] == data['code']), None)
        
        if not coupon:
            return jsonify({'success': False, 'error': 'Invalid coupon code'}), 404
        
        if not coupon.get('is_active', True):
            return jsonify({'success': False, 'error': 'Coupon is not active'}), 400
        
        # Check expiration
        expires_at = datetime.fromisoformat(coupon['expires_at'].replace('Z', '+00:00'))
        if expires_at <= datetime.now():
            return jsonify({'success': False, 'error': 'Coupon has expired'}), 400
        
        # Check usage limit
        if coupon['used_count'] >= coupon['usage_limit']:
            return jsonify({'success': False, 'error': 'Coupon usage limit reached'}), 400
        
        # Check minimum order amount
        if data['order_amount'] < coupon['min_order_amount']:
            return jsonify({'success': False, 'error': f'Minimum order amount is ${coupon["min_order_amount"]}'}), 400
        
        # Calculate discount
        if coupon['discount_type'] == 'percentage':
            discount_amount = data['order_amount'] * (coupon['discount_value'] / 100)
            discount_amount = min(discount_amount, coupon['max_discount'])
        else:  # fixed amount
            discount_amount = min(coupon['discount_value'], coupon['max_discount'])
        
        # FIX: Increment coupon used_count when successfully applied
        coupon_index = next((i for i, c in enumerate(coupons) if c['id'] == coupon['id']), None)
        if coupon_index is not None:
            coupons[coupon_index]['used_count'] = coupons[coupon_index].get('used_count', 0) + 1
            coupons[coupon_index]['last_used_at'] = datetime.now().isoformat()
            save_json('coupons.json', coupons)
        
        return jsonify({
            'success': True,
            'data': {
                'coupon_id': coupon['id'],
                'code': coupon['code'],
                'description': coupon['description'],
                'discount_amount': discount_amount,
                'discount_type': coupon['discount_type'],
                'final_amount': data['order_amount'] - discount_amount
            }
        }), 200
    
    @app.route('/api/coupons', methods=['POST'])
    @token_required
    @admin_required
    def create_coupon(user_data):
        """Create new coupon (Admin only)"""
        data = request.get_json()
        
        required_fields = ['code', 'description', 'discount_type', 'discount_value']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        if data['discount_type'] not in ['percentage', 'fixed']:
            return jsonify({'success': False, 'error': 'Invalid discount type'}), 400
        
        coupons = load_json('coupons.json')
        
        # Check if code already exists
        if any(c['code'] == data['code'] for c in coupons):
            return jsonify({'success': False, 'error': 'Coupon code already exists'}), 400
        
        new_coupon = {
            'id': get_next_id(coupons),
            'code': data['code'],
            'description': data['description'],
            'discount_type': data['discount_type'],
            'discount_value': data['discount_value'],
            'min_order_amount': data.get('min_order_amount', 0),
            'max_discount': data.get('max_discount', data['discount_value']),
            'usage_limit': data.get('usage_limit', 100),
            'used_count': 0,
            'expires_at': data.get('expires_at', (datetime.now() + timedelta(days=30)).isoformat()),
            'is_active': data.get('is_active', True),
            'created_at': datetime.now().isoformat()
        }
        
        coupons.append(new_coupon)
        save_json('coupons.json', coupons)
        
        return jsonify({
            'success': True,
            'message': 'Coupon created successfully',
            'data': new_coupon
        }), 201

# ============== NOTIFICATION SYSTEM ==============

def notification_routes(app):
    """Notification system routes"""
    
    @app.route('/api/notifications', methods=['GET'])
    @token_required
    def get_notifications(user_data):
        """Get user notifications"""
        user_id = user_data['id']
        
        notifications = load_json('notifications.json')
        user_notifications = [n for n in notifications if n['user_id'] == user_id]
        
        # Sort by creation date (newest first)
        user_notifications.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': user_notifications,
            'count': len(user_notifications),
            'unread_count': len([n for n in user_notifications if not n.get('is_read', False)])
        }), 200
    
    @app.route('/api/notifications/<int:notification_id>/read', methods=['PUT'])
    @token_required
    def mark_notification_read(user_data, notification_id):
        """Mark notification as read"""
        notifications = load_json('notifications.json')
        
        notification_index = next((i for i, n in enumerate(notifications) if n['id'] == notification_id), None)
        
        if notification_index is None:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        
        # Verify the notification belongs to the authenticated user
        if notifications[notification_index]['user_id'] != user_data['id']:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        notifications[notification_index]['is_read'] = True
        notifications[notification_index]['read_at'] = datetime.now().isoformat()
        
        save_json('notifications.json', notifications)
        
        return jsonify({
            'success': True,
            'message': 'Notification marked as read'
        }), 200
    
    @app.route('/api/notifications/read-all', methods=['PUT'])
    @token_required
    def mark_all_notifications_read(user_data):
        """Mark all user notifications as read"""
        user_id = user_data['id']
        
        notifications = load_json('notifications.json')
        
        updated_count = 0
        for notification in notifications:
            if notification['user_id'] == user_id and not notification.get('is_read', False):
                notification['is_read'] = True
                notification['read_at'] = datetime.now().isoformat()
                updated_count += 1
        
        save_json('notifications.json', notifications)
        
        return jsonify({
            'success': True,
            'message': f'{updated_count} notifications marked as read'
        }), 200

    @app.route('/api/notifications/test-create', methods=['POST'])
    @token_required
    def create_test_notifications(user_data):
        """Create random notifications for the authenticated user (testing only)"""
        data = request.get_json() or {}

        # Accept optional count parameter (default 1, max 100)
        try:
            count = int(data.get('count', 1))
        except Exception:
            return jsonify({'success': False, 'error': 'Invalid count value'}), 400

        if count < 1 or count > 100:
            return jsonify({'success': False, 'error': 'Count must be between 1 and 100'}), 400

        notifications = load_json('notifications.json')

        sample_titles = [
            'Order Update', 'Flash Sale', 'New Message', 'Shipping Notice',
            'Price Drop', 'Recommendation', 'Reminder', 'System Alert'
        ]

        created = []
        for _ in range(count):
            title = random.choice(sample_titles)
            body = f"{title}: This is a test notification at {datetime.now().isoformat()}"
            new_notification = {
                'id': get_next_id(notifications),
                'user_id': user_data['id'],
                'title': title,
                'body': body,
                'is_read': False,
                'created_at': datetime.now().isoformat()
            }
            notifications.append(new_notification)
            created.append(new_notification)

        save_json('notifications.json', notifications)

        return jsonify({
            'success': True,
            'message': f'Created {len(created)} test notification(s)',
            'data': created,
            'count': len(created)
        }), 201

# ============== ANALYTICS & REPORTING ==============

def analytics_routes(app):
    """Analytics and reporting routes"""
    
    @app.route('/api/analytics/dashboard', methods=['GET'])
    @token_required
    @admin_required
    def get_dashboard_analytics(user_data):
        """Get dashboard analytics (Admin only)"""
        analytics_data = load_json('analytics.json')
        
        # Calculate additional metrics
        users = load_json('users.json')
        products = load_json('products.json')
        orders = load_json('orders.json')
        
        # Sales metrics
        total_revenue = sum(o['total_amount'] for o in orders if o['status'] != 'cancelled')
        monthly_revenue = sum(o['total_amount'] for o in orders 
                           if o['status'] != 'cancelled' and 
                           datetime.fromisoformat(o['created_at']).month == datetime.now().month)
        
        # Popular products
        popular_products = []
        for pop_product in analytics_data['popular_products']:
            product = next((p for p in products if p['id'] == pop_product['product_id']), None)
            if product:
                popular_products.append({
                    'product': product,
                    'views': pop_product['views'],
                    'orders': pop_product['orders']
                })
        
        return jsonify({
            'success': True,
            'data': {
                'total_users': len(users),
                'total_products': len(products),
                'total_orders': len(orders),
                'total_revenue': total_revenue,
                'monthly_revenue': monthly_revenue,
                'popular_products': popular_products,
                'page_views_data': analytics_data['page_views'][-7:],  # Last 7 days
                'sales_data': analytics_data['sales_data'][-7:],  # Last 7 days
                'user_registrations': analytics_data['user_registrations'][-7:]  # Last 7 days
            }
        }), 200
    
    @app.route('/api/analytics/reports/sales', methods=['GET'])
    @token_required
    @admin_required
    def get_sales_report(user_data):
        """Get sales report with date filtering"""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        orders = load_json('orders.json')
        
        if start_date and end_date:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            filtered_orders = [o for o in orders 
                             if start_dt <= datetime.fromisoformat(o['created_at']) <= end_dt]
        else:
            filtered_orders = orders
        
        # Calculate metrics
        total_sales = sum(o['total_amount'] for o in filtered_orders if o['status'] != 'cancelled')
        total_orders = len(filtered_orders)
        cancelled_orders = len([o for o in filtered_orders if o['status'] == 'cancelled'])
        
        # Sales by status
        sales_by_status = {}
        for order in filtered_orders:
            status = order['status']
            if status not in sales_by_status:
                sales_by_status[status] = {'count': 0, 'revenue': 0}
            sales_by_status[status]['count'] += 1
            if status != 'cancelled':
                sales_by_status[status]['revenue'] += order['total_amount']
        
        return jsonify({
            'success': True,
            'data': {
                'period': {
                    'start_date': start_date,
                    'end_date': end_date
                },
                'summary': {
                    'total_sales': total_sales,
                    'total_orders': total_orders,
                    'cancelled_orders': cancelled_orders,
                    'average_order_value': total_sales / total_orders if total_orders > 0 else 0
                },
                'sales_by_status': sales_by_status,
                'orders': filtered_orders
            }
        }), 200

# ============== ADVANCED SEARCH ==============

def search_routes(app):
    """Advanced search functionality"""
    
    @app.route('/api/search/advanced', methods=['GET'])
    def advanced_search():
        """Advanced product search with multiple filters"""
        products = load_json('products.json')
        
        # Get search parameters
        query = request.args.get('q', '').lower()
        category = request.args.get('category')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        min_rating = request.args.get('min_rating', type=float)
        sort_by = request.args.get('sort_by', 'name')  # name, price, rating, newest
        sort_order = request.args.get('sort_order', 'asc')  # asc, desc
        
        filtered_products = products
        
        # Apply filters
        if query:
            filtered_products = [p for p in filtered_products 
                               if query in p.get('name', '').lower() or 
                               query in p.get('description', '').lower()]
        
        if category:
            filtered_products = [p for p in filtered_products if p.get('category', '').lower() == category.lower()]
        
        if min_price is not None:
            filtered_products = [p for p in filtered_products if p.get('price', 0) >= min_price]
        
        if max_price is not None:
            filtered_products = [p for p in filtered_products if p.get('price', 0) <= max_price]
        
        # Add average ratings (would need to calculate from reviews)
        reviews = load_json('reviews.json')
        for product in filtered_products:
            product_reviews = [r for r in reviews if r['product_id'] == product['id']]
            if product_reviews:
                product['average_rating'] = sum(r['rating'] for r in product_reviews) / len(product_reviews)
            else:
                product['average_rating'] = 0
        
        if min_rating is not None:
            filtered_products = [p for p in filtered_products if p.get('average_rating', 0) >= min_rating]
        
        # Sort results
        if sort_by == 'price':
            filtered_products.sort(key=lambda x: x.get('price', 0), reverse=(sort_order == 'desc'))
        elif sort_by == 'rating':
            filtered_products.sort(key=lambda x: x.get('average_rating', 0), reverse=(sort_order == 'desc'))
        elif sort_by == 'newest':
            filtered_products.sort(key=lambda x: x.get('created_at', ''), reverse=(sort_order == 'desc'))
        else:  # name
            filtered_products.sort(key=lambda x: x.get('name', ''), reverse=(sort_order == 'desc'))
        
        return jsonify({
            'success': True,
            'data': filtered_products,
            'count': len(filtered_products),
            'filters_applied': {
                'query': query,
                'category': category,
                'min_price': min_price,
                'max_price': max_price,
                'min_rating': min_rating,
                'sort_by': sort_by,
                'sort_order': sort_order
            }
        }), 200

# ============== PRODUCT RECOMMENDATIONS ==============

def recommendation_routes(app):
    """Product recommendation system"""
    
    @app.route('/api/recommendations/<int:product_id>', methods=['GET'])
    def get_product_recommendations(product_id):
        """Get recommended products based on a product"""
        products = load_json('products.json')
        target_product = next((p for p in products if p['id'] == product_id), None)
        
        if not target_product:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        # Simple recommendation: same category, different products
        category_products = [p for p in products 
                           if p['category'] == target_product['category'] and p['id'] != product_id]
        
        # Sort by price similarity (simple algorithm)
        target_price = target_product.get('price', 0)
        category_products.sort(key=lambda x: abs(x.get('price', 0) - target_price))
        
        # Return top 5 recommendations
        recommendations = category_products[:5]
        
        return jsonify({
            'success': True,
            'data': recommendations,
            'count': len(recommendations)
        }), 200
    
    @app.route('/api/recommendations/user/<int:user_id>', methods=['GET'])
    def get_user_recommendations(user_id):
        """Get personalized recommendations for user"""
        # Get user's order history
        orders = load_json('orders.json')
        user_orders = [o for o in orders if o['user_id'] == user_id and o['status'] != 'cancelled']
        
        if not user_orders:
            # No order history, return popular products
            products = load_json('products.json')
            analytics = load_json('analytics.json')
            
            popular_product_ids = [p['product_id'] for p in analytics['popular_products']]
            recommendations = [p for p in products if p['id'] in popular_product_ids][:5]
        else:
            # Get products from user's order history
            ordered_products = set()
            for order in user_orders:
                for item in order.get('items', []):
                    ordered_products.add(item['product_id'])
            
            # Find products in same categories
            products = load_json('products.json')
            ordered_categories = set()
            for product_id in ordered_products:
                product = next((p for p in products if p['id'] == product_id), None)
                if product:
                    ordered_categories.add(product['category'])
            
            # Get recommendations from same categories
            recommendations = []
            for product in products:
                if (product['id'] not in ordered_products and 
                    product['category'] in ordered_categories):
                    recommendations.append(product)
            
            # Limit to 5 recommendations
            recommendations = recommendations[:5]
        
        return jsonify({
            'success': True,
            'data': recommendations,
            'count': len(recommendations)
        }), 200

# ============== BLOG/CONTENT MANAGEMENT ==============

def blog_routes(app):
    """Blog and content management routes"""
    
    @app.route('/api/blog/posts', methods=['GET'])
    def get_blog_posts():
        """Get blog posts"""
        blog_posts = load_json('blog_posts.json')
        
        status = request.args.get('status', 'published')
        filtered_posts = [p for p in blog_posts if p.get('status') == status]
        
        # Sort by creation date (newest first)
        filtered_posts.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': filtered_posts,
            'count': len(filtered_posts)
        }), 200
    
    @app.route('/api/blog/posts/<int:post_id>', methods=['GET'])
    def get_blog_post(post_id):
        """Get specific blog post"""
        blog_posts = load_json('blog_posts.json')
        post = next((p for p in blog_posts if p['id'] == post_id), None)
        
        if not post:
            return jsonify({'success': False, 'error': 'Post not found'}), 404
        
        # Increment view count
        post['views'] = post.get('views', 0) + 1
        save_json('blog_posts.json', blog_posts)
        
        return jsonify({
            'success': True,
            'data': post
        }), 200

# ============== UTILITY FUNCTIONS ==============

def register_extended_routes(app):
    """Register all extended routes"""
    help_routes(app)
    contact_routes(app)
    wishlist_routes(app)
    coupon_routes(app)
    notification_routes(app)
    analytics_routes(app)
    search_routes(app)
    recommendation_routes(app)
    blog_routes(app)
