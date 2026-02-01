"""
Album routes with Swagger documentation.
"""
from flask import Blueprint
from flask_restx import Resource, fields

from app.routes import albums_ns as ns
from app.services import ytmusic, require_api_key
from app.middleware import success_response, error_response

bp = Blueprint('albums', __name__)


@ns.route('/<album_id>')
class Album(Resource):
    @ns.doc('get_album', security='apikey')
    @ns.response(200, 'Album info with all tracks')
    @ns.response(404, 'Album not found')
    @require_api_key
    def get(self, album_id):
        """Get album information including all tracks"""
        try:
            album = ytmusic.get_album(album_id)
            
            if not album:
                return error_response('ALBUM_NOT_FOUND', 'Album not found', 404)
            
            return success_response(album)
        except Exception as e:
            return error_response('ALBUM_ERROR', str(e), 500)


# Keep Flask blueprint route
@bp.route('/album/<album_id>', methods=['GET'])
@require_api_key
def get_album(album_id):
    try:
        album = ytmusic.get_album(album_id)
        if not album:
            return error_response('ALBUM_NOT_FOUND', 'Album not found', 404)
        return success_response(album)
    except Exception as e:
        return error_response('ALBUM_ERROR', str(e), 500)
