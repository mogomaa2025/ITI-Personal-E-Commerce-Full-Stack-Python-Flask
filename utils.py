import json
import os
import re
from config import Config
# How to do it (reusable helper functions)

def load_json(filename):
    """Load data from JSON file"""
    filepath = os.path.join(Config.DATA_DIR, filename)
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_json(filename, data):
    """Save data to JSON file"""
    filepath = os.path.join(Config.DATA_DIR, filename)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def get_next_id(data_list):
    """Get next available ID"""
    if not data_list:
        return 1
    return max(item['id'] for item in data_list) + 1

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def load_fail_config():
    """Load fail configuration for testing"""
    try:
        return load_json('fail.json')
    except:
        return {}

def apply_price_fail(total_price, fail_type='apitotalprice'):
    """Apply price calculation fail based on configuration"""
    fail_config = load_fail_config()
    price_config = fail_config.get('price', {})
    
    if price_config.get(fail_type, False):
        # Simulate developer error: convert to integer (truncate decimal)
        return int(total_price)
    
    return total_price

def cleanup_user_data(user_id):
    """Clean up all data associated with a user when they are deleted"""
    # List of all data files that contain user_id references
    data_files_to_clean = [
        'cart.json',          # Shopping cart items
        'orders.json',        # Order history
        'wishlist.json',      # Wishlist items
        'reviews.json',       # Product reviews
        'likes.json',         # Content likes
        'notifications.json', # User notifications
        'helpful_votes.json'  # Helpful votes (uses user_identifier)
    ]
    
    for filename in data_files_to_clean:
        try:
            data = load_json(filename)
            # Remove all entries that reference the deleted user_id
            if filename == 'helpful_votes.json':
                # Special handling for helpful_votes which uses user_identifier format
                updated_data = [item for item in data 
                               if item.get('user_identifier') != f'user_{user_id}']
            else:
                # Standard handling for files with user_id field
                updated_data = [item for item in data if item.get('user_id') != user_id]
            
            # Only save if changes were made
            if len(updated_data) != len(data):
                save_json(filename, updated_data)
                
        except Exception as e:
            # Continue with other files even if one fails
            pass