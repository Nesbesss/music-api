"""
Pytest configuration and fixtures.
"""
import pytest

from app import create_app, db
from app.config import TestingConfig
from app.models import APIKey


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def api_key(app):
    """Create a test API key."""
    with app.app_context():
        raw_key, key_obj = APIKey.create(
            name='Test Key',
            email='test@example.com',
            rate_limit=1000
        )
        return raw_key


@pytest.fixture
def auth_headers(api_key):
    """Headers with API key for authenticated requests."""
    return {'X-API-Key': api_key}


@pytest.fixture
def master_headers(app):
    """Headers with master key for admin requests."""
    return {'X-Master-Key': app.config['MASTER_API_KEY']}
