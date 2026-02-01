"""
Tests for search endpoints.
"""
import pytest


def test_search_requires_api_key(client):
    """Test that search requires API key."""
    response = client.get('/api/v1/search?q=test')
    assert response.status_code == 401
    assert response.json['error']['code'] == 'API_KEY_REQUIRED'


def test_search_without_query(client, auth_headers):
    """Test search without query parameter."""
    response = client.get('/api/v1/search', headers=auth_headers)
    assert response.status_code == 400
    assert response.json['error']['code'] == 'MISSING_QUERY'


def test_search_with_query(client, auth_headers, mocker):
    """Test search with valid query."""
    # Mock the ytmusic service
    mock_results = [
        {
            'id': 'abc123',
            'name': 'Test Song',
            'artists': [{'name': 'Test Artist'}],
            'album': {'name': 'Test Album', 'images': [{'url': 'http://example.com/img.jpg'}]},
            'duration_ms': 180000
        }
    ]
    
    mocker.patch('app.services.youtube_music.ytmusic.search', return_value=mock_results)
    
    response = client.get('/api/v1/search?q=test', headers=auth_headers)
    assert response.status_code == 200
    assert 'data' in response.json
    assert 'tracks' in response.json['data']
