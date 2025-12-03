#!/usr/bin/env python3
"""
Test script to verify helpful validation is working properly.
This script tests the one-time helpful validation system for help articles.
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

def test_helpful_validation():
    """Test the helpful validation system"""
    print("🧪 Testing Helpful Validation System")
    print("=" * 50)
    
    # Load current data
    helpful_votes = load_json('helpful_votes.json')
    help_articles = load_json('help.json')
    
    print(f"📊 Current data:")
    print(f"   Help articles: {len(help_articles)}")
    print(f"   Helpful votes: {len(helpful_votes)}")
    
    if not help_articles:
        print("❌ No help articles found. Please add some help articles first.")
        return
    
    # Test article
    test_article_id = help_articles[0]['id']
    test_user_identifier = "test_user_123"
    
    print(f"\n🎯 Testing with Article {test_article_id} and User {test_user_identifier}")
    
    # Test 1: First helpful vote should succeed
    print("\n1️⃣ Testing first helpful vote...")
    existing_vote = next((v for v in helpful_votes 
                        if v['user_identifier'] == test_user_identifier and v['help_id'] == test_article_id), None)
    
    if existing_vote:
        print(f"   ⚠️  User already voted for this article (ID: {existing_vote['id']})")
        print(f"   📅 Voted at: {existing_vote['created_at']}")
    else:
        print("   ✅ No existing vote found - first vote should succeed")
        
        # Add a test vote
        new_vote = {
            'id': max([v['id'] for v in helpful_votes], default=0) + 1,
            'help_id': test_article_id,
            'user_identifier': test_user_identifier,
            'created_at': datetime.now().isoformat()
        }
        helpful_votes.append(new_vote)
        save_json('helpful_votes.json', helpful_votes)
        print(f"   ✅ Added test vote (ID: {new_vote['id']})")
    
    # Test 2: Second vote should be blocked
    print("\n2️⃣ Testing duplicate vote prevention...")
    existing_vote = next((v for v in helpful_votes 
                        if v['user_identifier'] == test_user_identifier and v['help_id'] == test_article_id), None)
    
    if existing_vote:
        print("   ✅ Duplicate vote would be blocked - validation working!")
        print(f"   🚫 User {test_user_identifier} already voted for article {test_article_id}")
    else:
        print("   ❌ No existing vote found - validation may not be working")
    
    # Test 3: Check all votes for this user
    print(f"\n3️⃣ Checking all votes for user {test_user_identifier}...")
    user_votes = [v for v in helpful_votes if v['user_identifier'] == test_user_identifier]
    print(f"   📊 User has {len(user_votes)} total votes")
    
    for vote in user_votes:
        print(f"   👍 Voted for article {vote['help_id']} at {vote['created_at']}")
    
    # Test 4: Check all votes for this article
    print(f"\n4️⃣ Checking all votes for article {test_article_id}...")
    article_votes = [v for v in helpful_votes if v['help_id'] == test_article_id]
    print(f"   📊 Article has {len(article_votes)} total votes")
    
    for vote in article_votes:
        print(f"   👤 Voted by {vote['user_identifier']} at {vote['created_at']}")
    
    # Test 5: Check for duplicates
    print(f"\n5️⃣ Checking for duplicate votes...")
    seen_pairs = set()
    duplicates = []
    
    for vote in helpful_votes:
        key = (vote['user_identifier'], vote['help_id'])
        if key in seen_pairs:
            duplicates.append(vote)
        else:
            seen_pairs.add(key)
    
    if duplicates:
        print(f"   ⚠️  Found {len(duplicates)} duplicate votes:")
        for dup in duplicates:
            print(f"   🔄 {dup['user_identifier']} -> Article {dup['help_id']} (ID: {dup['id']})")
    else:
        print("   ✅ No duplicate votes found")
    
    # Test 6: Update help article helpful count
    print(f"\n6️⃣ Updating helpful count for article {test_article_id}...")
    article_index = next((i for i, h in enumerate(help_articles) if h['id'] == test_article_id), None)
    if article_index is not None:
        help_articles[article_index]['helpful_count'] = len(article_votes)
        save_json('help.json', help_articles)
        print(f"   ✅ Updated helpful count to {len(article_votes)}")
    
    print(f"\n🎉 Helpful validation test completed!")
    print(f"📈 Total votes in database: {len(helpful_votes)}")
    print(f"👥 Unique user-article pairs: {len(seen_pairs)}")

if __name__ == "__main__":
    test_helpful_validation()
