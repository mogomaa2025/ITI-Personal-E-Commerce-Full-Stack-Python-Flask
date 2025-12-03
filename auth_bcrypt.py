import jwt
import bcrypt
from datetime import datetime, timedelta
from config import Config
#This  handles user authentication and password security

#Convert password to bcrypt hash for storage (PRODUCTION-READY)
def hash_password(password):
    """Hash password using bcrypt (industry standard)"""
    # Generate salt and hash password
    salt = bcrypt.gensalt(rounds=12)  # 12 rounds = good balance of security/performance
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Store as string in JSON

#Check if password matches stored hash
def verify_password(password, hashed_password):
    """Verify password against bcrypt hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

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