"""
Artist routes with Swagger documentation.
"""
from flask import Blueprint
from flask_restx import Resource, fields

from app.routes import artists_ns as ns
from app.services import ytmusic, require_api_key
from app.middleware import success_response, error_response

bp = Blueprint('artists', __name__)


@ns.route('/<artist_id>')
class Artist(Resource):
    @ns.doc('get_artist', security='apikey')
    @ns.response(200, 'Artist info with top songs and albums')
    @ns.response(404, 'Artist not found')
    @require_api_key
    def get(self, artist_id):
        """Get artist information including top songs and albums"""
        try:
            artist = ytmusic.get_artist(artist_id)
            
            if not artist:
                return error_response('ARTIST_NOT_FOUND', 'Artist not found', 404)
            
            return success_response(artist)
        except Exception as e:
            return error_response('ARTIST_ERROR', str(e), 500)


# Keep Flask blueprint route
@bp.route('/artist/<artist_id>', methods=['GET'])
@require_api_key
def get_artist(artist_id):
    try:
        artist = ytmusic.get_artist(artist_id)
        if not artist:
            return error_response('ARTIST_NOT_FOUND', 'Artist not found', 404)
        return success_response(artist)
    except Exception as e:
        return error_response('ARTIST_ERROR', str(e), 500)
