import os
from datetime import timedelta
# Central place for all application settings and keys. 🔑

class Config:
    """Application configuration"""

    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key-change-in-production'
    
    # JWT Access Token Expiration: 24 hours (PRODUCTION-READY)
    # Changed from 480 hours (20 days) to 24 hours for security
    # Use refresh token for extended sessions
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # 24 hours
    
    # JWT Refresh Token Expiration: 30 days
    # Refresh tokens allow users to get new access tokens without re-login
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 30 days

    # JSON database settings
    DATA_DIR = os.environ.get('DATA_DIR') or os.path.join(_BASE_DIR, 'data')

    # CORS settings
    CORS_HEADERS = 'Content-Type'
