"""
Health check routes with Swagger documentation.
"""
from flask import Blueprint, current_app
from flask_restx import Resource, fields

from app.routes import health_ns as ns
from app.services.cache import cache
from app.middleware import success_response

bp = Blueprint('health', __name__)


# Models for Swagger
health_response = ns.model('HealthResponse', {
    'data': fields.Nested(ns.model('HealthData', {
        'status': fields.String(description='Service status'),
        'service': fields.String(description='Service name'),
        'version': fields.String(description='API version'),
        'components': fields.Nested(ns.model('Components', {
            'database': fields.String(),
            'cache': fields.String()
        }))
    }))
})


@ns.route('')
class Health(Resource):
    @ns.doc('health_check')
    @ns.response(200, 'Service is healthy', health_response)
    def get(self):
        """Health check endpoint - no auth required"""
        # Check Redis
        redis_status = 'connected'
        try:
            redis_client = cache._get_redis()
            if redis_client:
                redis_client.ping()
            else:
                redis_status = 'not configured (using memory cache)'
        except Exception as e:
            redis_status = f'error: {e}'
        
        # Check database
        db_status = 'connected'
        try:
            from app import db
            db.session.execute(db.text('SELECT 1'))
        except Exception as e:
            db_status = f'error: {e}'
        
        return success_response({
            'status': 'ok',
            'service': 'music-api',
            'version': '1.0.0',
            'components': {
                'database': db_status,
                'cache': redis_status
            }
        })


# Keep Flask blueprint route
@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    redis_status = 'connected'
    try:
        redis_client = cache._get_redis()
        if redis_client:
            redis_client.ping()
        else:
            redis_status = 'not configured (using memory cache)'
    except Exception as e:
        redis_status = f'error: {e}'
    
    db_status = 'connected'
    try:
        from app import db
        db.session.execute(db.text('SELECT 1'))
    except Exception as e:
        db_status = f'error: {e}'
    
    return success_response({
        'status': 'ok',
        'service': 'music-api',
        'version': '1.0.0',
        'components': {
            'database': db_status,
            'cache': redis_status
        }
    })
