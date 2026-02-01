"""
Error handling middleware with consistent response format.
"""
import uuid
from flask import jsonify, request, current_app
from werkzeug.exceptions import HTTPException


def generate_request_id() -> str:
    """Generate a unique request ID for tracing."""
    return str(uuid.uuid4())[:8]


def error_response(code: str, message: str, status_code: int = 400, details: dict = None):
    """Create a consistent error response."""
    request_id = getattr(request, 'request_id', generate_request_id())
    
    response = {
        'error': {
            'code': code,
            'message': message,
            'request_id': request_id
        }
    }
    
    if details:
        response['error']['details'] = details
    
    return response, status_code


def success_response(data: dict, status_code: int = 200, meta: dict = None):
    """Create a consistent success response."""
    request_id = getattr(request, 'request_id', generate_request_id())
    
    response = {
        'data': data,
        'meta': {
            'request_id': request_id,
            **(meta or {})
        }
    }
    
    return response, status_code


def register_error_handlers(app):
    """Register error handlers for the Flask app."""
    
    @app.before_request
    def add_request_id():
        """Add a unique request ID to each request."""
        request.request_id = generate_request_id()
    
    @app.after_request
    def add_request_id_header(response):
        """Add request ID to response headers."""
        if hasattr(request, 'request_id'):
            response.headers['X-Request-ID'] = request.request_id
        return response
    
    @app.errorhandler(400)
    def bad_request(error):
        return error_response('BAD_REQUEST', str(error.description), 400)
    
    @app.errorhandler(401)
    def unauthorized(error):
        return error_response('UNAUTHORIZED', 'Authentication required', 401)
    
    @app.errorhandler(403)
    def forbidden(error):
        return error_response('FORBIDDEN', 'Access denied', 403)
    
    @app.errorhandler(404)
    def not_found(error):
        return error_response('NOT_FOUND', 'Resource not found', 404)
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return error_response('METHOD_NOT_ALLOWED', 'Method not allowed', 405)
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return error_response('RATE_LIMIT_EXCEEDED', 'Too many requests, please slow down', 429)
    
    @app.errorhandler(500)
    def internal_error(error):
        current_app.logger.error(f"Internal error: {error}")
        return error_response('INTERNAL_ERROR', 'An unexpected error occurred', 500)
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle uncaught exceptions."""
        if isinstance(error, HTTPException):
            return error_response(
                error.name.upper().replace(' ', '_'),
                error.description,
                error.code
            )
        
        current_app.logger.exception(f"Unhandled exception: {error}")
        return error_response('INTERNAL_ERROR', 'An unexpected error occurred', 500)
