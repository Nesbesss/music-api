"""
Search routes with Swagger documentation.
"""
from flask import Blueprint, request
from flask_restx import Resource, fields

from app.routes import search_ns as ns
from app.services import ytmusic, require_api_key
from app.middleware import success_response, error_response

bp = Blueprint('search', __name__)

# Models for Swagger
track_model = ns.model('Track', {
    'id': fields.String(description='Video ID'),
    'name': fields.String(description='Track name'),
    'artists': fields.List(fields.Nested(ns.model('Artist', {
        'name': fields.String(),
        'id': fields.String()
    }))),
    'album': fields.Nested(ns.model('Album', {
        'name': fields.String(),
        'images': fields.List(fields.Nested(ns.model('Image', {
            'url': fields.String()
        })))
    })),
    'duration_ms': fields.Integer(description='Duration in milliseconds')
})

search_response = ns.model('SearchResponse', {
    'data': fields.Nested(ns.model('SearchData', {
        'tracks': fields.List(fields.Nested(track_model)),
        'total': fields.Integer()
    }))
})


@ns.route('')
class Search(Resource):
    @ns.doc('search_tracks', security='apikey')
    @ns.param('q', 'Search query', required=True)
    @ns.param('limit', 'Number of results (max 50)', default=20)
    @ns.response(200, 'Success', search_response)
    @ns.response(400, 'Missing query parameter')
    @ns.response(401, 'API key required')
    @require_api_key
    def get(self):
        """Search for tracks on YouTube Music"""
        query = request.args.get('q', '')
        limit = min(int(request.args.get('limit', 20)), 50)
        
        if not query:
            return error_response('MISSING_QUERY', 'Query parameter "q" is required', 400)
        
        try:
            results = ytmusic.search(query, limit=limit)
            
                
            return success_response({
                'tracks': results,
                'total': len(results)
            })
        except Exception as e:
            return error_response('SEARCH_ERROR', str(e), 500)


# Keep Flask blueprint route for backwards compatibility
@bp.route('/search', methods=['GET'])
@require_api_key
def search():
    """Search for tracks on YouTube Music"""
    query = request.args.get('q', '')
    limit = min(int(request.args.get('limit', 20)), 50)
    
    if not query:
        return error_response('MISSING_QUERY', 'Query parameter "q" is required', 400)
    
    try:
        results = ytmusic.search(query, limit=limit)
        

        return success_response({
            'tracks': results,
            'total': len(results)
        })
    except Exception as e:
        return error_response('SEARCH_ERROR', str(e), 500)
