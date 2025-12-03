import json
import os
import random

def load_json(filename):
    """Load data from JSON file"""
    filepath = os.path.join('data', filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'Error: {filename} not found in data directory')
        return []

def save_json(filename, data):
    """Save data to JSON file"""
    filepath = os.path.join('data', filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'✓ Saved {filename}')

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

def migrate_product_images():
    """Migrate existing product images from external URLs to local images"""
    print('=' * 60)
    print('PRODUCT IMAGE MIGRATION')
    print('=' * 60)
    print()
    
    # Load products
    products = load_json('products.json')
    
    if not products:
        print('No products found to migrate.')
        return
    
    updated_count = 0
    
    # Update each product's image_url
    for product in products:
        old_url = product.get('image_url', '')
        
        # Only update if it's an external URL
        if old_url.startswith('http'):
            category = product.get('category', '')
            new_url = get_local_image_for_category(category)
            product['image_url'] = new_url
            updated_count += 1
            print(f'✓ Updated: {product["name"]} -> {new_url}')
    
    # Save updated products
    if updated_count > 0:
        save_json('products.json', products)
        print()
        print('=' * 60)
        print(f'MIGRATION COMPLETE')
        print(f'Updated {updated_count} product(s)')
        print('=' * 60)
    else:
        print('No external URLs found. All products already use local images.')

if __name__ == '__main__':
    migrate_product_images()
