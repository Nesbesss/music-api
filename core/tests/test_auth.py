"""
Tests for authentication and API key management.
"""
import pytest


def test_health_no_auth_required(client):
    """Test health endpoint doesn't require auth."""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert response.json['data']['status'] == 'ok'


def test_invalid_api_key(client):
    """Test request with invalid API key."""
    response = client.get('/api/v1/search?q=test', headers={'X-API-Key': 'invalid-key'})
    assert response.status_code == 401
    assert response.json['error']['code'] == 'INVALID_API_KEY'


def test_create_api_key(client, master_headers):
    """Test creating a new API key."""
    response = client.post('/api/v1/admin/keys', 
        json={'name': 'New App', 'email': 'app@example.com'},
        headers=master_headers
    )
    assert response.status_code == 201
    assert 'key' in response.json['data']
    assert response.json['data']['name'] == 'New App'


def test_create_api_key_requires_master_key(client):
    """Test that creating API key requires master key."""
    response = client.post('/api/v1/admin/keys', 
        json={'name': 'New App', 'email': 'app@example.com'}
    )
    assert response.status_code == 401


def test_list_api_keys(client, master_headers, api_key):
    """Test listing all API keys."""
    response = client.get('/api/v1/admin/keys', headers=master_headers)
    assert response.status_code == 200
    assert response.json['data']['total'] >= 1


def test_revoke_api_key(client, master_headers, app):
    """Test revoking an API key."""
    from app.models import APIKey
    
    with app.app_context():
        raw_key, key_obj = APIKey.create('Temp Key', 'temp@example.com')
        key_id = key_obj.id
    
    response = client.delete(f'/api/v1/admin/keys/{key_id}', headers=master_headers)
    assert response.status_code == 200
    
    # Try to use revoked key
    response = client.get('/api/v1/search?q=test', headers={'X-API-Key': raw_key})
    assert response.status_code == 401
