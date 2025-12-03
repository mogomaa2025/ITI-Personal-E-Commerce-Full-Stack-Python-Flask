#!/usr/bin/env python3
"""
Cleanup script to remove duplicate likes from the database.
This ensures that each user can only like each product once.
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

def cleanup_duplicate_likes():
    """Remove duplicate likes from the database"""
    print("🧹 Starting cleanup of duplicate likes...")
    
    # Load current likes
    likes = load_json('likes.json')
    print(f"📊 Found {len(likes)} total likes")
    
    if not likes:
        print("✅ No likes found, nothing to clean up")
        return
    
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
            print(f"🗑️  Removing duplicate like: User {like['user_id']} -> Product {like['product_id']}")
    
    # Save cleaned data
    save_json('likes.json', unique_likes)
    
    print(f"✅ Cleanup completed!")
    print(f"📈 Removed {duplicates_removed} duplicate likes")
    print(f"📊 Remaining unique likes: {len(unique_likes)}")
    
    # Show statistics
    if unique_likes:
        user_likes = {}
        product_likes = {}
        
        for like in unique_likes:
            user_id = like['user_id']
            product_id = like['product_id']
            
            user_likes[user_id] = user_likes.get(user_id, 0) + 1
            product_likes[product_id] = product_likes.get(product_id, 0) + 1
        
        print(f"\n📊 Statistics:")
        print(f"👥 Users who liked products: {len(user_likes)}")
        print(f"🛍️  Products that were liked: {len(product_likes)}")
        print(f"🔥 Most liked product: {max(product_likes.items(), key=lambda x: x[1]) if product_likes else 'None'}")
        print(f"👤 Most active liker: {max(user_likes.items(), key=lambda x: x[1]) if user_likes else 'None'}")

if __name__ == "__main__":
    cleanup_duplicate_likes()
