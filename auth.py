import jwt
import hashlib
from datetime import datetime, timedelta
from config import Config

# FALLBACK TO SHA256 due to Windows bcrypt DLL issue
# TODO: Fix bcrypt DLL (see BCRYPT_WINDOWS_FIX.md) and use auth_bcrypt.py
# NOTE: auth_bcrypt.py has the production-ready bcrypt version

#This  handles user authentication and password security

#Convert password to SHA256 hash for storage (FALLBACK - bcrypt preferred)
def hash_password(password):
    """Hash password using SHA256 (FALLBACK until bcrypt DLL fixed)"""
    # NOTE: This is a fallback. Bcrypt version available in auth_bcrypt.py
    return hashlib.sha256(password.encode()).hexdigest()

#Check if password matches stored hash
def verify_password(password, hashed_password):
    """Verify password against SHA256 hash"""
    return hash_password(password) == hashed_password

#Create JWT access token for authenticated users
def generate_token(user_id, email, is_admin=False):
    """Generate JWT access token"""
    payload = {
        'id': user_id,
        'email': email,
        'is_admin': is_admin,
        'type': 'access',
        'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
    }
    
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    return token

#Create JWT refresh token for token refresh mechanism
def generate_refresh_token(user_id, email):
    """Generate JWT refresh token (longer expiration)"""
    payload = {
        'id': user_id,
        'email': email,
        'type': 'refresh',
        'exp': datetime.utcnow() + Config.JWT_REFRESH_TOKEN_EXPIRES
    }
    
    refresh_token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    return refresh_token

#Validate JWT token and extract user data
def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

"""
User Registration/Login Flow:
┌─────────────────────────────────────┐
│ User enters password                 │
├─────────────────────────────────────┤
│ hash_password() → SHA256 hash        │
│ Store hash in database               │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ User logs in with password           │
├─────────────────────────────────────┤
│ verify_password() → Compare hashes   │
│ If match → generate_token()          │
│ Return JWT token to client           │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│ Client sends token in API requests   │
├─────────────────────────────────────┤
│ verify_token() → Decode & validate   │
│ If valid → Allow request             │
│ If expired/invalid → Deny request    │
└─────────────────────────────────────┘
Security Features:
- Password hashing - Never stores plain passwords
- JWT tokens - Stateless authentication
- Token expiration - 20-days validity (change from config.py)
- Admin flag - Role-based access control
"""