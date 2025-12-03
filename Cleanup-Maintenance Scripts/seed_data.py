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
PRODUCTS_DATA = {
    'Electronics': [
        ('Laptop Pro 15"', 'High-performance laptop with 16GB RAM and 512GB SSD', 1299.99, 'https://via.placeholder.com/400x300/3498db/ffffff?text=Laptop'),
        ('Wireless Mouse', 'Ergonomic wireless mouse with precision tracking', 29.99, 'https://via.placeholder.com/400x300/2ecc71/ffffff?text=Mouse'),
        ('Mechanical Keyboard', 'RGB mechanical keyboard with Cherry MX switches', 149.99, 'https://via.placeholder.com/400x300/e74c3c/ffffff?text=Keyboard'),
        ('4K Monitor 27"', 'Ultra HD 4K monitor with HDR support', 449.99, 'https://via.placeholder.com/400x300/9b59b6/ffffff?text=Monitor'),
        ('USB-C Hub', '7-in-1 USB-C hub with HDMI and ethernet', 59.99, 'https://via.placeholder.com/400x300/f39c12/ffffff?text=USB+Hub'),
        ('Webcam HD', '1080p HD webcam with auto-focus', 79.99, 'https://via.placeholder.com/400x300/1abc9c/ffffff?text=Webcam'),
        ('Bluetooth Speaker', 'Portable waterproof Bluetooth speaker', 89.99, 'https://via.placeholder.com/400x300/34495e/ffffff?text=Speaker'),
        ('Wireless Earbuds', 'True wireless earbuds with active noise cancellation', 199.99, 'https://via.placeholder.com/400x300/16a085/ffffff?text=Earbuds'),
        ('Gaming Headset', 'Pro gaming headset with 7.1 surround sound', 129.99, 'https://via.placeholder.com/400x300/c0392b/ffffff?text=Headset'),
        ('Portable SSD 1TB', 'External solid state drive 1TB', 149.99, 'https://via.placeholder.com/400x300/2c3e50/ffffff?text=SSD'),
        ('Smart Watch', 'Fitness tracker smart watch with heart rate monitor', 249.99, 'https://via.placeholder.com/400x300/8e44ad/ffffff?text=Watch'),
        ('Tablet 10"', 'Android tablet with 64GB storage', 299.99, 'https://via.placeholder.com/400x300/27ae60/ffffff?text=Tablet'),
        ('Power Bank 20000mAh', 'Fast charging power bank', 39.99, 'https://via.placeholder.com/400x300/d35400/ffffff?text=Power+Bank'),
        ('HDMI Cable 10ft', 'Premium 4K HDMI cable', 19.99, 'https://via.placeholder.com/400x300/7f8c8d/ffffff?text=HDMI'),
        ('Laptop Stand', 'Adjustable aluminum laptop stand', 49.99, 'https://via.placeholder.com/400x300/95a5a6/ffffff?text=Stand'),
    ],
    'Clothing': [
        ('Classic T-Shirt', 'Comfortable cotton t-shirt', 19.99, 'https://via.placeholder.com/400x300/3498db/ffffff?text=T-Shirt'),
        ('Denim Jeans', 'Slim fit denim jeans', 59.99, 'https://via.placeholder.com/400x300/2ecc71/ffffff?text=Jeans'),
        ('Leather Jacket', 'Genuine leather jacket', 199.99, 'https://via.placeholder.com/400x300/e74c3c/ffffff?text=Jacket'),
        ('Running Shoes', 'Lightweight running shoes', 89.99, 'https://via.placeholder.com/400x300/9b59b6/ffffff?text=Shoes'),
        ('Hoodie', 'Warm fleece hoodie', 49.99, 'https://via.placeholder.com/400x300/f39c12/ffffff?text=Hoodie'),
        ('Polo Shirt', 'Classic polo shirt', 34.99, 'https://via.placeholder.com/400x300/1abc9c/ffffff?text=Polo'),
        ('Cargo Pants', 'Multi-pocket cargo pants', 54.99, 'https://via.placeholder.com/400x300/34495e/ffffff?text=Cargo'),
        ('Winter Coat', 'Insulated winter coat', 149.99, 'https://via.placeholder.com/400x300/16a085/ffffff?text=Coat'),
        ('Baseball Cap', 'Adjustable baseball cap', 24.99, 'https://via.placeholder.com/400x300/c0392b/ffffff?text=Cap'),
        ('Sneakers', 'Casual canvas sneakers', 64.99, 'https://via.placeholder.com/400x300/2c3e50/ffffff?text=Sneakers'),
        ('Dress Shirt', 'Formal dress shirt', 44.99, 'https://via.placeholder.com/400x300/8e44ad/ffffff?text=Dress+Shirt'),
        ('Chino Pants', 'Slim fit chino pants', 49.99, 'https://via.placeholder.com/400x300/27ae60/ffffff?text=Chinos'),
        ('Bomber Jacket', 'Lightweight bomber jacket', 79.99, 'https://via.placeholder.com/400x300/d35400/ffffff?text=Bomber'),
        ('Athletic Shorts', 'Breathable athletic shorts', 29.99, 'https://via.placeholder.com/400x300/7f8c8d/ffffff?text=Shorts'),
        ('Wool Sweater', 'Warm wool sweater', 69.99, 'https://via.placeholder.com/400x300/95a5a6/ffffff?text=Sweater'),
    ],
    'Books': [
        ('Python Programming Guide', 'Complete guide to Python programming', 39.99, 'https://via.placeholder.com/400x300/3498db/ffffff?text=Python+Book'),
        ('Mystery Novel Collection', 'Set of 3 bestselling mystery novels', 29.99, 'https://via.placeholder.com/400x300/2ecc71/ffffff?text=Mystery'),
        ('Science Fiction Anthology', 'Classic sci-fi short stories', 24.99, 'https://via.placeholder.com/400x300/e74c3c/ffffff?text=Sci-Fi'),
        ('Cooking Masterclass', 'Professional cooking techniques', 34.99, 'https://via.placeholder.com/400x300/9b59b6/ffffff?text=Cooking'),
        ('Fitness & Nutrition', 'Complete guide to healthy living', 27.99, 'https://via.placeholder.com/400x300/f39c12/ffffff?text=Fitness'),
        ('Business Strategy', 'Modern business management strategies', 44.99, 'https://via.placeholder.com/400x300/1abc9c/ffffff?text=Business'),
        ('Graphic Design Basics', 'Introduction to graphic design', 32.99, 'https://via.placeholder.com/400x300/34495e/ffffff?text=Design'),
        ('World History', 'Comprehensive world history textbook', 49.99, 'https://via.placeholder.com/400x300/16a085/ffffff?text=History'),
        ('Photography Guide', 'Digital photography for beginners', 36.99, 'https://via.placeholder.com/400x300/c0392b/ffffff?text=Photo'),
        ('Self-Help Classic', 'Life-changing self-improvement book', 22.99, 'https://via.placeholder.com/400x300/2c3e50/ffffff?text=Self-Help'),
        ('Travel Guide Europe', 'Complete European travel guide', 31.99, 'https://via.placeholder.com/400x300/8e44ad/ffffff?text=Travel'),
        ('Children Story Collection', 'Classic bedtime stories for kids', 19.99, 'https://via.placeholder.com/400x300/27ae60/ffffff?text=Kids'),
        ('Biography Collection', 'Inspiring life stories', 28.99, 'https://via.placeholder.com/400x300/d35400/ffffff?text=Biography'),
        ('Philosophy Essentials', 'Introduction to philosophy', 38.99, 'https://via.placeholder.com/400x300/7f8c8d/ffffff?text=Philosophy'),
        ('Art History', 'Survey of Western art history', 42.99, 'https://via.placeholder.com/400x300/95a5a6/ffffff?text=Art'),
    ],
    'Home & Garden': [
        ('Coffee Maker', 'Programmable 12-cup coffee maker', 79.99, 'https://via.placeholder.com/400x300/3498db/ffffff?text=Coffee+Maker'),
        ('Blender Pro', 'High-speed blender for smoothies', 129.99, 'https://via.placeholder.com/400x300/2ecc71/ffffff?text=Blender'),
        ('Garden Hose 50ft', 'Expandable garden hose', 34.99, 'https://via.placeholder.com/400x300/e74c3c/ffffff?text=Hose'),
        ('LED Desk Lamp', 'Adjustable LED desk lamp', 44.99, 'https://via.placeholder.com/400x300/9b59b6/ffffff?text=Lamp'),
        ('Storage Bins Set', 'Set of 6 plastic storage bins', 39.99, 'https://via.placeholder.com/400x300/f39c12/ffffff?text=Bins'),
        ('Vacuum Cleaner', 'Bagless upright vacuum cleaner', 149.99, 'https://via.placeholder.com/400x300/1abc9c/ffffff?text=Vacuum'),
        ('Cookware Set', '10-piece non-stick cookware set', 199.99, 'https://via.placeholder.com/400x300/34495e/ffffff?text=Cookware'),
        ('Bath Towel Set', 'Set of 6 premium cotton towels', 49.99, 'https://via.placeholder.com/400x300/16a085/ffffff?text=Towels'),
        ('Plant Pots Set', 'Ceramic plant pots with drainage', 29.99, 'https://via.placeholder.com/400x300/c0392b/ffffff?text=Pots'),
        ('Tool Set', '100-piece home repair tool set', 89.99, 'https://via.placeholder.com/400x300/2c3e50/ffffff?text=Tools'),
        ('Bed Sheet Set', 'Queen size microfiber sheet set', 54.99, 'https://via.placeholder.com/400x300/8e44ad/ffffff?text=Sheets'),
        ('Wall Clock', 'Modern minimalist wall clock', 39.99, 'https://via.placeholder.com/400x300/27ae60/ffffff?text=Clock'),
        ('Cutting Board Set', 'Bamboo cutting board set of 3', 34.99, 'https://via.placeholder.com/400x300/d35400/ffffff?text=Cutting+Board'),
        ('Shower Curtain', 'Waterproof fabric shower curtain', 24.99, 'https://via.placeholder.com/400x300/7f8c8d/ffffff?text=Curtain'),
        ('Garden Tools Kit', 'Essential gardening tools kit', 64.99, 'https://via.placeholder.com/400x300/95a5a6/ffffff?text=Garden+Tools'),
    ],
    'Sports': [
        ('Yoga Mat', 'Non-slip exercise yoga mat', 29.99, 'https://via.placeholder.com/400x300/3498db/ffffff?text=Yoga+Mat'),
        ('Dumbbell Set', 'Adjustable dumbbell set 50lbs', 149.99, 'https://via.placeholder.com/400x300/2ecc71/ffffff?text=Dumbbells'),
        ('Resistance Bands', 'Set of 5 resistance bands', 24.99, 'https://via.placeholder.com/400x300/e74c3c/ffffff?text=Bands'),
        ('Jump Rope', 'Speed jump rope for cardio', 14.99, 'https://via.placeholder.com/400x300/9b59b6/ffffff?text=Jump+Rope'),
        ('Basketball', 'Official size basketball', 34.99, 'https://via.placeholder.com/400x300/f39c12/ffffff?text=Basketball'),
        ('Soccer Ball', 'Professional soccer ball size 5', 29.99, 'https://via.placeholder.com/400x300/1abc9c/ffffff?text=Soccer'),
        ('Tennis Racket', 'Lightweight tennis racket', 79.99, 'https://via.placeholder.com/400x300/34495e/ffffff?text=Racket'),
        ('Bicycle Helmet', 'Safety certified bike helmet', 49.99, 'https://via.placeholder.com/400x300/16a085/ffffff?text=Helmet'),
        ('Water Bottle 32oz', 'Insulated stainless steel bottle', 24.99, 'https://via.placeholder.com/400x300/c0392b/ffffff?text=Bottle'),
        ('Gym Bag', 'Durable sports gym bag', 44.99, 'https://via.placeholder.com/400x300/2c3e50/ffffff?text=Gym+Bag'),
        ('Boxing Gloves', 'Training boxing gloves 12oz', 54.99, 'https://via.placeholder.com/400x300/8e44ad/ffffff?text=Gloves'),
        ('Skateboard', 'Complete skateboard for beginners', 69.99, 'https://via.placeholder.com/400x300/27ae60/ffffff?text=Skateboard'),
        ('Badminton Set', 'Complete badminton set with net', 59.99, 'https://via.placeholder.com/400x300/d35400/ffffff?text=Badminton'),
        ('Swimming Goggles', 'Anti-fog swimming goggles', 19.99, 'https://via.placeholder.com/400x300/7f8c8d/ffffff?text=Goggles'),
        ('Fitness Tracker', 'Basic fitness activity tracker', 39.99, 'https://via.placeholder.com/400x300/95a5a6/ffffff?text=Tracker'),
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

def get_random_image_url(width=400, height=300, category=None):
    """
    Generate a random image URL using reliable services
    
    Args:
        width (int): Image width in pixels
        height (int): Image height in pixels
        category (str): Optional category keyword (not used but kept for compatibility)
    
    Returns:
        str: Random image URL
    """
    # Use reliable image services
    services = [
        # Picsum Photos with random seeds
        f"https://picsum.photos/{width}/{height}?random={random.randint(1, 1000)}",
        f"https://picsum.photos/{width}/{height}?random={random.randint(1, 1000)}",
        
        # DummyImage service - very reliable
        f"https://dummyimage.com/{width}x{height}/3498db/ffffff&text=Product",
        f"https://dummyimage.com/{width}x{height}/2ecc71/ffffff&text=Product",
        f"https://dummyimage.com/{width}x{height}/e74c3c/ffffff&text=Product",
        f"https://dummyimage.com/{width}x{height}/9b59b6/ffffff&text=Product",
        f"https://dummyimage.com/{width}x{height}/f39c12/ffffff&text=Product",
        f"https://dummyimage.com/{width}x{height}/1abc9c/ffffff&text=Product",
        f"https://dummyimage.com/{width}x{height}/34495e/ffffff&text=Product",
        f"https://dummyimage.com/{width}x{height}/16a085/ffffff&text=Product",
        f"https://dummyimage.com/{width}x{height}/c0392b/ffffff&text=Product",
        f"https://dummyimage.com/{width}x{height}/2c3e50/ffffff&text=Product",
    ]
    
    return random.choice(services)

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
        for name, description, price, _ in items:  # Ignore the old image_url
            # Generate random image URL based on category
            keywords = category_keywords.get(category, [])
            if keywords:
                keyword = random.choice(keywords)
                image_url = get_random_image_url(category=keyword)
            else:
                image_url = get_random_image_url()
            
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
