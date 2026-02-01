"""
Configuration settings for the Music API.
"""
import os
from pathlib import Path


class Config:
    """Base configuration."""
    
    # Base directory
    BASE_DIR = Path(__file__).parent.parent
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/music_api.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Keys
    MASTER_API_KEY = os.getenv('MASTER_API_KEY', 'dev-master-key')
    ALLOW_ANONYMOUS_ACCESS = os.getenv('ALLOW_ANONYMOUS_ACCESS', 'true').lower() == 'true'
    
    # Redis (optional)
    REDIS_URL = os.getenv('REDIS_URL', None)
    
    # Rate Limiting
    RATE_LIMIT_DEFAULT = os.getenv('RATE_LIMIT_DEFAULT', '100/minute')
    RATE_LIMIT_SEARCH = os.getenv('RATE_LIMIT_SEARCH', '30/minute')
    
    # Cache TTL (seconds)
    CACHE_TTL_SEARCH = 300  # 5 minutes
    CACHE_TTL_TRACK = 3600  # 1 hour
    CACHE_TTL_RECOMMENDATIONS = 1800  # 30 minutes
    CACHE_TTL_ARTIST = 3600  # 1 hour
    CACHE_TTL_ALBUM = 3600  # 1 hour
    
    # Service URLs (for cross-linking in Docker/Production)
    API_URL = os.getenv('API_URL', 'http://localhost:5001')
    DASHBOARD_URL = os.getenv('DASHBOARD_URL', 'http://localhost:5002')
    API_DOCS_URL = os.getenv('API_DOCS_URL', 'http://localhost:5003')
    
    # Whisper
    WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'base')
    WHISPER_DEVICE = os.getenv('WHISPER_DEVICE', 'cpu')
    WHISPER_COMPUTE_TYPE = os.getenv('WHISPER_COMPUTE_TYPE', 'int8')
    
    # Directories
    LYRICS_CACHE_DIR = BASE_DIR / 'cache' / 'lyrics'
    DOWNLOADS_DIR = BASE_DIR / 'downloads'


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Stricter rate limits in production
    RATE_LIMIT_DEFAULT = os.getenv('RATE_LIMIT_DEFAULT', '60/minute')
    RATE_LIMIT_SEARCH = os.getenv('RATE_LIMIT_SEARCH', '20/minute')


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # No rate limiting in tests
    RATE_LIMIT_DEFAULT = '1000/minute'
    RATE_LIMIT_SEARCH = '1000/minute'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment."""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
