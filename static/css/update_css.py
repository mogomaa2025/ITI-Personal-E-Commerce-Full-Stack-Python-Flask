with open('style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Update line 218: background-color -> background gradient
lines[217] = '    background: linear-gradient(135deg, #dc3545 0%, #c0392b 100%);\r\n'

# Update line 220: color from red to white
lines[219] = '    color: white;\r\n'

# Update line 221: box-shadow
lines[220] = '    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);\r\n'

# Update line 225 in hover: background gradient -> transparent 
lines[224] = '    background-color: transparent;\r\n'

# Insert new line after 225 for border
lines.insert(225, '    border: 2px solid #dc3545;\r\n')

# Update line 227 (now 228): color from white to red
lines[227] = '    color: #dc3545;\r\n'

with open('style.css', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Updated successfully!")
