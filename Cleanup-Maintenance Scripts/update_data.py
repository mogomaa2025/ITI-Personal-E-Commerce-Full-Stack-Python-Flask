import json
import os
import random
from datetime import datetime, timedelta

def load_json(filename):
    """Load data from JSON file"""
    filepath = os.path.join('data', filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_json(filename, data):
    """Save data to JSON file"""
    filepath = os.path.join('data', filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def add_products(category, count=10):
    """Add more products to a specific category"""
    products = load_json('products.json')
    
    next_id = max([p['id'] for p in products]) + 1 if products else 1
    
    product_templates = {
        'Electronics': ('Device', 'Electronic device with advanced features'),
        'Clothing': ('Apparel', 'Quality clothing item'),
        'Books': ('Book', 'Interesting reading material'),
        'Home & Garden': ('Item', 'Useful home item'),
        'Sports': ('Equipment', 'Sports equipment')
    }
    
    template_name, template_desc = product_templates.get(category, ('Product', 'Quality product'))
    
    for i in range(count):
        products.append({
            'id': next_id + i,
            'name': f'{template_name} {next_id + i}',
            'description': f'{template_desc} - Product ID {next_id + i}',
            'price': round(random.uniform(9.99, 999.99), 2),
            'category': category,
            'stock': random.randint(10, 200),
            'image_url': f'https://via.placeholder.com/400x300/3498db/ffffff?text=Product+{next_id + i}',
            'created_at': datetime.now().isoformat()
        })
    
    save_json('products.json', products)
    print(f'✓ Added {count} products to {category} category')
    print(f'Total products: {len(products)}')

if __name__ == '__main__':
    print('Add More Products')
    print('=' * 40)
    print('Categories: Electronics, Clothing, Books, Home & Garden, Sports')
    
    category = input('Enter category: ')
    count = int(input('How many products to add? '))
    
    add_products(category, count)
