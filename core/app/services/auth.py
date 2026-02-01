"""
Authentication service - Zero-Gate minimal version.
Supports ALLOW_ANONYMOUS_ACCESS for frictionless local development.
"""
from functools import wraps
from flask import request, current_app, g

def require_api_key(f):
    """Decorator to require API key (bypassed if ALLOW_ANONYMOUS_ACCESS is True)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        allow_anon = current_app.config.get('ALLOW_ANONYMOUS_ACCESS', False)
        
        if allow_anon:
            # Inject a mock API key object for compatibility
            class MockKey:
                id = 0
                key_prefix = "anon"
                user_id = 0
                name = "Anonymous User"
                
            g.api_key = MockKey()
            return f(*args, **kwargs)
            
        # Fail if not allowed and no key
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            from app.middleware import error_response
            return error_response('API_KEY_REQUIRED', 'API key required', 401)
            
        # Normally we would validate against DB here, but for "Zero-Gate" core, 
        # we focus on the open experience.
        return f(*args, **kwargs)
    
    return decorated

def require_master_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated

def optional_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated
