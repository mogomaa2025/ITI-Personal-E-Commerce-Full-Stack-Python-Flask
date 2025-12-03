import os
import json

def clear_all_data():
    """Clear all JSON database files"""
    files = ['users.json', 'products.json', 'categories.json', 
             'orders.json', 'reviews.json', 'cart.json']
    
    print('Clearing all data files...')
    
    for filename in files:
        filepath = os.path.join('data', filename)
        if os.path.exists(filepath):
            with open(filepath, 'w') as f:
                json.dump([], f)
            print(f'✓ Cleared {filename}')
    
    print('\n✓ All data cleared successfully!')
    print('Run "python seed_data.py" to regenerate test data.')

if __name__ == '__main__':
    response = input('Are you sure you want to clear all data? (yes/no): ')
    if response.lower() == 'yes':
        clear_all_data()
    else:
        print('Operation cancelled.')
