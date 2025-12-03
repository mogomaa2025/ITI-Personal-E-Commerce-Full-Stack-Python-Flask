import json
import random

# Category to local images mapping
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

# Load products
with open('data/products.json', 'r') as f:
    products = json.load(f)

updated_count = 0

# Update each product
for product in products:
    old_url = product.get('image_url', '')
    
    # Only update if it's an external URL
    if old_url.startswith('http'):
        category = product.get('category', '')
        images = category_images.get(category, ['/static/img/placeholder.svg'])
        new_url = random.choice(images)
        product['image_url'] = new_url
        updated_count += 1

# Save
with open('data/products.json', 'w') as f:
    json.dump(products, f, indent=4)

print(f'Updated {updated_count} products')
