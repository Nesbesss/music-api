"""
Usage logging middleware.
"""
import time
from flask import request, g
from app.models.usage import UsageLog

def register_usage_logger(app):
    """Register usage logging middleware."""
    
    @app.before_request
    def start_timer():
        g.start_time = time.time()
    
    @app.after_request
    def log_request_metrics(response):
        # Only log if we have an API Key (authenticated request)
        if hasattr(g, 'api_key') and g.api_key:
            try:
                # Calculate duration
                duration = 0
                if hasattr(g, 'start_time'):
                    duration = int((time.time() - g.start_time) * 1000)
                
                # Log to DB
                UsageLog.log_request(
                    api_key_id=g.api_key.id,
                    endpoint=request.path,
                    method=request.method,
                    status_code=response.status_code,
                    response_time_ms=duration
                )
            except Exception as e:
                # Don't fail the request if logging fails
                app.logger.error(f"Failed to log usage: {e}")
                
        return response
