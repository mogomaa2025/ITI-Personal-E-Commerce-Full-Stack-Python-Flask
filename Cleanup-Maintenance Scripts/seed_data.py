import json
import os
import random
from datetime import datetime, timedelta
import hashlib

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def random_date(start_days_ago=365, end_days_ago=0):
    """Generate random date"""
    start = datetime.now() - timedelta(days=start_days_ago)
    end = datetime.now() - timedelta(days=end_days_ago)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).isoformat()

# Sample data
FIRST_NAMES = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emma', 'James', 'Olivia', 
               'Robert', 'Sophia', 'William', 'Isabella', 'Richard', 'Mia', 'Thomas', 
               'Charlotte', 'Daniel', 'Amelia', 'Matthew', 'Emily']

LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
              'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 
              'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']

STREETS = ['Main St', 'Oak Ave', 'Maple Dr', 'Cedar Ln', 'Park Blvd', 'Washington St',
           'Lake View Dr', 'Highland Ave', 'Sunset Blvd', 'River Rd']

CITIES = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
          'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
          'Fort Worth', 'Columbus', 'San Francisco', 'Charlotte', 'Indianapolis',
          'Seattle', 'Denver', 'Boston']

# Product data by category
# Product data by category - using local images from static/img
PRODUCTS_DATA = {
    'Electronics': [
        ('Laptop Pro 15"', 'High-performance laptop with 16GB RAM and 512GB SSD', 1299.99, '/static/img/laptop.png'),
        ('Wireless Mouse', 'Ergonomic wireless mouse with precision tracking', 29.99, '/static/img/mouse.png'),
        ('Mechanical Keyboard', 'RGB mechanical keyboard with Cherry MX switches', 149.99, '/static/img/keyboard.png'),
        ('4K Monitor 27"', 'Ultra HD 4K monitor with HDR support', 449.99, '/static/img/mointor.png'),
        ('USB-C Hub', '7-in-1 USB-C hub with HDMI and ethernet', 59.99, '/static/img/usbhub.png'),
        ('Webcam HD', '1080p HD webcam with auto-focus', 79.99, '/static/img/cam.png'),
        ('Bluetooth Speaker', 'Portable waterproof Bluetooth speaker', 89.99, '/static/img/speaker.png'),
        ('Wireless Earbuds', 'True wireless earbuds with active noise cancellation', 199.99, '/static/img/other.png'),
        ('Gaming Headset', 'Pro gaming headset with 7.1 surround sound', 129.99, '/static/img/other.png'),
        ('Portable SSD 1TB', 'External solid state drive 1TB', 149.99, '/static/img/other.png'),
        ('Smart Watch', 'Fitness tracker smart watch with heart rate monitor', 249.99, '/static/img/other.png'),
        ('Tablet 10"', 'Android tablet with 64GB storage', 299.99, '/static/img/other.png'),
        ('Power Bank 20000mAh', 'Fast charging power bank', 39.99, '/static/img/other.png'),
        ('HDMI Cable 10ft', 'Premium 4K HDMI cable', 19.99, '/static/img/other.png'),
        ('Laptop Stand', 'Adjustable aluminum laptop stand', 49.99, '/static/img/other.png'),
    ],
    'Clothing': [
        ('Classic T-Shirt', 'Comfortable cotton t-shirt', 19.99, '/static/img/other.png'),
        ('Denim Jeans', 'Slim fit denim jeans', 59.99, '/static/img/other.png'),
        ('Leather Jacket', 'Genuine leather jacket', 199.99, '/static/img/other.png'),
        ('Running Shoes', 'Lightweight running shoes', 89.99, '/static/img/other.png'),
        ('Hoodie', 'Warm fleece hoodie', 49.99, '/static/img/other.png'),
        ('Polo Shirt', 'Classic polo shirt', 34.99, '/static/img/other.png'),
        ('Cargo Pants', 'Multi-pocket cargo pants', 54.99, '/static/img/other.png'),
        ('Winter Coat', 'Insulated winter coat', 149.99, '/static/img/other.png'),
        ('Baseball Cap', 'Adjustable baseball cap', 24.99, '/static/img/other.png'),
        ('Sneakers', 'Casual canvas sneakers', 64.99, '/static/img/other.png'),
        ('Dress Shirt', 'Formal dress shirt', 44.99, '/static/img/other.png'),
        ('Chino Pants', 'Slim fit chino pants', 49.99, '/static/img/other.png'),
        ('Bomber Jacket', 'Lightweight bomber jacket', 79.99, '/static/img/other.png'),
        ('Athletic Shorts', 'Breathable athletic shorts', 29.99, '/static/img/other.png'),
        ('Wool Sweater', 'Warm wool sweater', 69.99, '/static/img/other.png'),
    ],
    'Books': [
        ('Python Programming Guide', 'Complete guide to Python programming', 39.99, '/static/img/other.png'),
        ('Mystery Novel Collection', 'Set of 3 bestselling mystery novels', 29.99, '/static/img/other.png'),
        ('Science Fiction Anthology', 'Classic sci-fi short stories', 24.99, '/static/img/other.png'),
        ('Cooking Masterclass', 'Professional cooking techniques', 34.99, '/static/img/other.png'),
        ('Fitness & Nutrition', 'Complete guide to healthy living', 27.99, '/static/img/other.png'),
        ('Business Strategy', 'Modern business management strategies', 44.99, '/static/img/other.png'),
        ('Graphic Design Basics', 'Introduction to graphic design', 32.99, '/static/img/other.png'),
        ('World History', 'Comprehensive world history textbook', 49.99, '/static/img/other.png'),
        ('Photography Guide', 'Digital photography for beginners', 36.99, '/static/img/other.png'),
        ('Self-Help Classic', 'Life-changing self-improvement book', 22.99, '/static/img/other.png'),
        ('Travel Guide Europe', 'Complete European travel guide', 31.99, '/static/img/other.png'),
        ('Children Story Collection', 'Classic bedtime stories for kids', 19.99, '/static/img/other.png'),
        ('Biography Collection', 'Inspiring life stories', 28.99, '/static/img/other.png'),
        ('Philosophy Essentials', 'Introduction to philosophy', 38.99, '/static/img/other.png'),
        ('Art History', 'Survey of Western art history', 42.99, '/static/img/other.png'),
    ],
    'Home & Garden': [
        ('Coffee Maker', 'Programmable 12-cup coffee maker', 79.99, '/static/img/other.png'),
        ('Blender Pro', 'High-speed blender for smoothies', 129.99, '/static/img/other.png'),
        ('Garden Hose 50ft', 'Expandable garden hose', 34.99, '/static/img/other.png'),
        ('LED Desk Lamp', 'Adjustable LED desk lamp', 44.99, '/static/img/other.png'),
        ('Storage Bins Set', 'Set of 6 plastic storage bins', 39.99, '/static/img/other.png'),
        ('Vacuum Cleaner', 'Bagless upright vacuum cleaner', 149.99, '/static/img/other.png'),
        ('Cookware Set', '10-piece non-stick cookware set', 199.99, '/static/img/other.png'),
        ('Bath Towel Set', 'Set of 6 premium cotton towels', 49.99, '/static/img/other.png'),
        ('Plant Pots Set', 'Ceramic plant pots with drainage', 29.99, '/static/img/other.png'),
        ('Tool Set', '100-piece home repair tool set', 89.99, '/static/img/other.png'),
        ('Bed Sheet Set', 'Queen size microfiber sheet set', 54.99, '/static/img/other.png'),
        ('Wall Clock', 'Modern minimalist wall clock', 39.99, '/static/img/other.png'),
        ('Cutting Board Set', 'Bamboo cutting board set of 3', 34.99, '/static/img/other.png'),
        ('Shower Curtain', 'Waterproof fabric shower curtain', 24.99, '/static/img/other.png'),
        ('Garden Tools Kit', 'Essential gardening tools kit', 64.99, '/static/img/other.png'),
    ],
    'Sports': [
        ('Yoga Mat', 'Non-slip exercise yoga mat', 29.99, '/static/img/other.png'),
        ('Dumbbell Set', 'Adjustable dumbbell set 50lbs', 149.99, '/static/img/other.png'),
        ('Resistance Bands', 'Set of 5 resistance bands', 24.99, '/static/img/other.png'),
        ('Jump Rope', 'Speed jump rope for cardio', 14.99, '/static/img/other.png'),
        ('Basketball', 'Official size basketball', 34.99, '/static/img/other.png'),
        ('Soccer Ball', 'Professional soccer ball size 5', 29.99, '/static/img/other.png'),
        ('Tennis Racket', 'Lightweight tennis racket', 79.99, '/static/img/other.png'),
        ('Bicycle Helmet', 'Safety certified bike helmet', 49.99, '/static/img/other.png'),
        ('Water Bottle 32oz', 'Insulated stainless steel bottle', 24.99, '/static/img/other.png'),
        ('Gym Bag', 'Durable sports gym bag', 44.99, '/static/img/other.png'),
        ('Boxing Gloves', 'Training boxing gloves 12oz', 54.99, '/static/img/other.png'),
        ('Skateboard', 'Complete skateboard for beginners', 69.99, '/static/img/other.png'),
        ('Badminton Set', 'Complete badminton set with net', 59.99, '/static/img/other.png'),
        ('Swimming Goggles', 'Anti-fog swimming goggles', 19.99, '/static/img/other.png'),
        ('Fitness Tracker', 'Basic fitness activity tracker', 39.99, '/static/img/other.png'),
    ]
}

REVIEW_COMMENTS = [
    'Excellent product! Highly recommended.',
    'Great quality for the price.',
    'Fast shipping and well packaged.',
    'Exceeded my expectations!',
    'Good value for money.',
    'Works perfectly as described.',
    'Very satisfied with this purchase.',
    'Amazing product, will buy again!',
    'Decent quality, does the job.',
    'Pretty good, but could be better.',
    'Average product, nothing special.',
    'Not bad, but not great either.',
    'Could use some improvements.',
    'Disappointed with the quality.',
    'Not as described, returning it.',
    'Poor quality, not worth the price.',
    'Excellent build quality and design.',
    'Perfect for my needs!',
    'My family loves it!',
    'Best purchase I made this year.',
    'Solid product, no complaints.',
    'Works great, easy to use.',
    'Stylish and functional.',
    'Comfortable and durable.',
    'Good product overall.',
]

ORDER_STATUSES = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

def get_local_image_for_category(category):
    """
    Get a local image path from static/img based on category
    
    Args:
        category (str): Product category name
    
    Returns:
        str: Local image path
    """
    # Map categories to available local images
    category_images = {
        'Electronics': [
            '/static/img/laptop.png',
            '/static/img/mouse.png',
            '/static/img/keyboard.png',
            '/static/img/mointor.png',
            '/static/img/speaker.png',
            '/static/img/cam.png',
            '/static/img/usbhub.png'
        ],
        'Clothing': ['/static/img/other.png'],
        'Books': ['/static/img/other.png'],
        'Home & Garden': ['/static/img/other.png'],
        'Sports': ['/static/img/other.png']
    }
    
    images = category_images.get(category, ['/static/img/placeholder.svg'])
    return random.choice(images)

def get_category_keywords():
    """
    Get relevant keywords for each product category
    """
    return {
        'Electronics': ['technology', 'computer', 'gadget', 'device', 'electronic'],
        'Clothing': ['fashion', 'clothing', 'style', 'wear', 'apparel'],
        'Books': ['book', 'reading', 'literature', 'education', 'study'],
        'Home & Garden': ['home', 'house', 'garden', 'interior', 'decor'],
        'Sports': ['sport', 'fitness', 'exercise', 'athletic', 'workout']
    }

def generate_users(count=30):
    """Generate random users"""
    users = []
    
    # Add admin user
    users.append({
        'id': 1,
        'email': 'admin@test.com',
        'password': hash_password('admin123'),
        'name': 'Admin User',
        'phone': '555-0100',
        'address': f'{random.randint(100, 999)} {random.choice(STREETS)}, {random.choice(CITIES)}, NY 10001',
        'is_admin': True,
        'created_at': random_date(365, 180)
    })
    
    # Add test user
    users.append({
        'id': 2,
        'email': 'user@test.com',
        'password': hash_password('user123'),
        'name': 'Test User',
        'phone': '555-0101',
        'address': f'{random.randint(100, 999)} {random.choice(STREETS)}, {random.choice(CITIES)}, CA 90001',
        'is_admin': False,
        'created_at': random_date(365, 90)
    })
    
    # Generate additional users
    for i in range(3, count + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        
        users.append({
            'id': i,
            'email': f'{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@email.com',
            'password': hash_password('password123'),
            'name': f'{first_name} {last_name}',
            'phone': f'555-{random.randint(1000, 9999)}',
            'address': f'{random.randint(100, 999)} {random.choice(STREETS)}, {random.choice(CITIES)}, {random.choice(["NY", "CA", "TX", "FL"])} {random.randint(10000, 99999)}',
            'is_admin': False,
            'created_at': random_date(365, 0)
        })
    
    return users

def generate_products():
    """Generate products from predefined data"""
    products = []
    product_id = 1
    category_keywords = get_category_keywords()
    
    for category, items in PRODUCTS_DATA.items():
        for name, description, price, image_url in items:  # Use the image_url from PRODUCTS_DATA
            # image_url is now already set from PRODUCTS_DATA with local paths
            
            products.append({
                'id': product_id,
                'name': name,
                'description': description,
                'price': price,
                'category': category,
                'stock': random.randint(10, 200),
                'image_url': image_url,
                'created_at': random_date(180, 0)
            })
            product_id += 1
    
    return products

def generate_categories():
    """Generate categories"""
    categories = [
        {
            'id': 1,
            'name': 'Electronics',
            'description': 'Electronic devices and accessories',
            'created_at': random_date(365, 300)
        },
        {
            'id': 2,
            'name': 'Clothing',
            'description': 'Fashion and apparel',
            'created_at': random_date(365, 300)
        },
        {
            'id': 3,
            'name': 'Books',
            'description': 'Books and publications',
            'created_at': random_date(365, 300)
        },
        {
            'id': 4,
            'name': 'Home & Garden',
            'description': 'Home improvement and garden supplies',
            'created_at': random_date(365, 300)
        },
        {
            'id': 5,
            'name': 'Sports',
            'description': 'Sports equipment and accessories',
            'created_at': random_date(365, 300)
        }
    ]
    
    return categories

def generate_orders(users, products, count=50):
    """Generate random orders"""
    orders = []
    
    for i in range(1, count + 1):
        user = random.choice([u for u in users if not u['is_admin']])
        num_items = random.randint(1, 5)
        selected_products = random.sample(products, num_items)
        
        order_items = []
        total_amount = 0
        
        for product in selected_products:
            quantity = random.randint(1, 3)
            subtotal = product['price'] * quantity
            total_amount += subtotal
            
            order_items.append({
                'product_id': product['id'],
                'product_name': product['name'],
                'quantity': quantity,
                'price': product['price'],
                'subtotal': subtotal
            })
        
        status = random.choices(
            ORDER_STATUSES,
            weights=[10, 20, 30, 35, 5],  # More delivered/shipped orders
            k=1
        )[0]
        
        order_date = random_date(90, 0)
        
        order = {
            'id': i,
            'user_id': user['id'],
            'items': order_items,
            'total_amount': round(total_amount, 2),
            'status': status,
            'shipping_address': user['address'],
            'created_at': order_date
        }
        
        if status in ['shipped', 'delivered']:
            order['updated_at'] = random_date(
                (datetime.now() - datetime.fromisoformat(order_date)).days,
                0
            )
        
        if status == 'cancelled':
            order['cancelled_at'] = random_date(
                (datetime.now() - datetime.fromisoformat(order_date)).days,
                0
            )
        
        orders.append(order)
    
    return orders

def generate_reviews(users, products, count=100):
    """Generate random product reviews"""
    reviews = []
    reviewed_combinations = set()
    
    for i in range(1, count + 1):
        # Ensure unique user-product combinations
        while True:
            user = random.choice([u for u in users if not u['is_admin']])
            product = random.choice(products)
            combo = (user['id'], product['id'])
            
            if combo not in reviewed_combinations:
                reviewed_combinations.add(combo)
                break
        
        rating = random.choices(
            [1, 2, 3, 4, 5],
            weights=[5, 10, 15, 35, 35],  # More positive reviews
            k=1
        )[0]
        
        reviews.append({
            'id': i,
            'user_id': user['id'],
            'product_id': product['id'],
            'rating': rating,
            'comment': random.choice(REVIEW_COMMENTS),
            'created_at': random_date(60, 0)
        })
    
    return reviews

def generate_cart_items(users, products, count=20):
    """Generate random cart items"""
    cart_items = []
    
    for i in range(1, count + 1):
        user = random.choice([u for u in users if not u['is_admin']])
        product = random.choice(products)
        
        cart_items.append({
            'id': i,
            'user_id': user['id'],
            'product_id': product['id'],
            'quantity': random.randint(1, 5),
            'created_at': random_date(7, 0)
        })
    
    return cart_items

def save_json(filename, data):
    """Save data to JSON file"""
    filepath = os.path.join('data', filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'✓ Created {filename} with {len(data)} records')

def main():
    """Main function to generate all test data"""
    print('=' * 60)
    print('E-COMMERCE TEST DATA GENERATOR')
    print('=' * 60)
    print()
    
    print('Generating test data...')
    print()
    
    # Generate data
    users = generate_users(30)
    products = generate_products()
    categories = generate_categories()
    orders = generate_orders(users, products, 50)
    reviews = generate_reviews(users, products, 100)
    cart_items = generate_cart_items(users, products, 20)
    
    # Save to files
    save_json('users.json', users)
    save_json('products.json', products)
    save_json('categories.json', categories)
    save_json('orders.json', orders)
    save_json('reviews.json', reviews)
    save_json('cart.json', cart_items)
    
    print()
    print('=' * 60)
    print('SUMMARY')
    print('=' * 60)
    print(f'Users: {len(users)} (including 1 admin, 1 test user)')
    print(f'Products: {len(products)} across {len(categories)} categories')
    print(f'Orders: {len(orders)}')
    print(f'Reviews: {len(reviews)}')
    print(f'Cart Items: {len(cart_items)}')
    print()
    print('TEST CREDENTIALS')
    print('=' * 60)
    print('Admin Account:')
    print('  Email: admin@test.com')
    print('  Password: admin123')
    print()
    print('Test User Account:')
    print('  Email: user@test.com')
    print('  Password: user123')
    print()
    print('Other Users:')
    print('  Password for all: password123')
    print()
    print('✓ Test data generation completed successfully!')
    print('✓ Run "python app.py" to start the server')
    print('=' * 60)

if __name__ == '__main__':
    main()
