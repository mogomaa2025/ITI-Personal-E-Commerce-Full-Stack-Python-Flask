import re

# Read the CSS file
with open('style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace btn-outline default styling
content = content.replace(
    '''.btn-outline {
    background-color: transparent;
    border: 2px solid #dc3545;
    color: #dc3545;
    box-shadow: none;
}''',
    '''.btn-outline {
    background: linear-gradient(135deg, #dc3545 0%, #c0392b 100%);
    border: 2px solid #dc3545;
    color: white;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}''')

# Replace btn-outline hover styling  
content = content.replace(
    '''.btn-outline:hover {
    background: linear-gradient(135deg, #dc3545 0%, #c0392b 100%);
    color: white;
}''',
    '''.btn-outline:hover {
    background-color: transparent;
    border: 2px solid #dc3545;
    color: #dc3545;
}''')

# Write back
with open('style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated btn-outline styling!")
