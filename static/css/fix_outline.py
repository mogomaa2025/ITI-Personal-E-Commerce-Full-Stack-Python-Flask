# Read the file
with open('style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and replace line 218 (background-color)
if lines[217].strip() == 'background-color: transparent;':
    lines[217] = '    background: linear-gradient(135deg, #dc3545 0%, #c0392b 100%);\r\n'

# Find and replace line 220 (color)
if lines[219].strip().startswith('color: #dc3545'):
    lines[219] = '    color: white;\r\n'

# Find and replace line 221 (box-shadow)
if lines[220].strip() == 'box-shadow: none;':
    lines[220] = '    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);\r\n'

# Update hover state (lines 224-226)
if lines[224].strip().startswith('background: linear-gradient'):
    lines[224] = '    background-color: transparent;\r\n'
if 'border:' not in lines[225].strip() and lines[225].strip().startswith('color: white'):
    lines[225] = '    border: 2px solid #dc3545;\r\n'
    lines.insert(226, '    color: #dc3545;\r\n')

# Write back
with open('style.css', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("CSS updated successfully!")
