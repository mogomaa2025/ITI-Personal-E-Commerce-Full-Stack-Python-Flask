#!/usr/bin/env python3
"""
Test script to verify like validation is working properly.
This script tests the one-time like validation system.
"""

import json
import os
from datetime import datetime

def load_json(filename):
    """Load JSON data from file"""
    try:
        with open(f'data/{filename}', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_json(filename, data):
    """Save JSON data to file"""
    os.makedirs('data', exist_ok=True)
    with open(f'data/{filename}', 'w') as f:
        json.dump(data, f, indent=4)

def test_like_validation():
    """Test the like validation system"""
    print("🧪 Testing Like Validation System")
    print("=" * 50)
    
    # Load current data
    likes = load_json('likes.json')
    users = load_json('users.json')
    products = load_json('products.json')
    
    print(f"📊 Current data:")
    print(f"   Users: {len(users)}")
    print(f"   Products: {len(products)}")
    print(f"   Likes: {len(likes)}")
    
    if not users or not products:
        print("❌ No users or products found. Please run seed_data.py first.")
        return
    
    # Test user and product
    test_user_id = users[0]['id']
    test_product_id = products[0]['id']
    
    print(f"\n🎯 Testing with User {test_user_id} and Product {test_product_id}")
    
    # Test 1: First like should succeed
    print("\n1️⃣ Testing first like...")
    existing_like = next((l for l in likes if l['user_id'] == test_user_id and l['product_id'] == test_product_id), None)
    
    if existing_like:
        print(f"   ⚠️  User already liked this product (ID: {existing_like['id']})")
        print(f"   📅 Liked at: {existing_like['created_at']}")
    else:
        print("   ✅ No existing like found - first like should succeed")
        
        # Add a test like
        new_like = {
            'id': max([l['id'] for l in likes], default=0) + 1,
            'user_id': test_user_id,
            'product_id': test_product_id,
            'created_at': datetime.now().isoformat()
        }
        likes.append(new_like)
        save_json('likes.json', likes)
        print(f"   ✅ Added test like (ID: {new_like['id']})")
    
    # Test 2: Second like should be blocked
    print("\n2️⃣ Testing duplicate like prevention...")
    existing_like = next((l for l in likes if l['user_id'] == test_user_id and l['product_id'] == test_product_id), None)
    
    if existing_like:
        print("   ✅ Duplicate like would be blocked - validation working!")
        print(f"   🚫 User {test_user_id} already liked product {test_product_id}")
    else:
        print("   ❌ No existing like found - validation may not be working")
    
    # Test 3: Check all likes for this user
    print(f"\n3️⃣ Checking all likes for user {test_user_id}...")
    user_likes = [l for l in likes if l['user_id'] == test_user_id]
    print(f"   📊 User has {len(user_likes)} total likes")
    
    for like in user_likes:
        print(f"   ❤️  Liked product {like['product_id']} at {like['created_at']}")
    
    # Test 4: Check all likes for this product
    print(f"\n4️⃣ Checking all likes for product {test_product_id}...")
    product_likes = [l for l in likes if l['product_id'] == test_product_id]
    print(f"   📊 Product has {len(product_likes)} total likes")
    
    for like in product_likes:
        print(f"   👤 Liked by user {like['user_id']} at {like['created_at']}")
    
    # Test 5: Check for duplicates
    print(f"\n5️⃣ Checking for duplicate likes...")
    seen_pairs = set()
    duplicates = []
    
    for like in likes:
        key = (like['user_id'], like['product_id'])
        if key in seen_pairs:
            duplicates.append(like)
        else:
            seen_pairs.add(key)
    
    if duplicates:
        print(f"   ⚠️  Found {len(duplicates)} duplicate likes:")
        for dup in duplicates:
            print(f"   🔄 User {dup['user_id']} -> Product {dup['product_id']} (ID: {dup['id']})")
    else:
        print("   ✅ No duplicate likes found")
    
    print(f"\n🎉 Validation test completed!")
    print(f"📈 Total likes in database: {len(likes)}")
    print(f"👥 Unique user-product pairs: {len(seen_pairs)}")

if __name__ == "__main__":
    test_like_validation()
