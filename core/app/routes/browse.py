"""
Browse routes with Swagger documentation - trending, genres, recommendations.
"""
from flask import Blueprint, request
from flask_restx import Resource, fields

from app.routes import browse_ns as ns
from app.services import ytmusic, require_api_key
from app.middleware import success_response, error_response

bp = Blueprint('browse', __name__)


@ns.route('/recommendations/<video_id>')
class Recommendations(Resource):
    @ns.doc('get_recommendations', security='apikey')
    @ns.param('limit', 'Number of results (max 50)', default=20)
    @ns.response(200, 'Related tracks')
    @require_api_key
    def get(self, video_id):
        """Get song recommendations based on a video"""
        limit = min(int(request.args.get('limit', 20)), 50)
        
        try:
            tracks = ytmusic.get_recommendations(video_id, limit=limit)
            return success_response({
                'tracks': tracks,
                'total': len(tracks)
            })
        except Exception as e:
            return error_response('RECOMMENDATIONS_ERROR', str(e), 500)


@ns.route('/trending')
class Trending(Resource):
    @ns.doc('get_trending', security='apikey')
    @ns.param('region', 'ISO country code (e.g., US, GB, NL)', default='US')
    @ns.response(200, 'Trending tracks')
    @require_api_key
    def get(self):
        """Get trending/chart songs by region"""
        region = request.args.get('region', 'US').upper()
        
        try:
            tracks = ytmusic.get_trending(region)
            return success_response({
                'tracks': tracks,
                'total': len(tracks),
                'region': region
            })
        except Exception as e:
            return error_response('TRENDING_ERROR', str(e), 500)


@ns.route('/genres')
class Genres(Resource):
    @ns.doc('get_genres', security='apikey')
    @ns.response(200, 'List of genres and moods')
    @require_api_key
    def get(self):
        """Get available mood/genre categories"""
        try:
            genres = ytmusic.get_genres()
            return success_response({
                'genres': genres,
                'total': len(genres)
            })
        except Exception as e:
            return error_response('GENRES_ERROR', str(e), 500)


@ns.route('/genres/<genre_id>')
class GenrePlaylists(Resource):
    @ns.doc('get_genre_playlists', security='apikey')
    @ns.response(200, 'Playlists in the genre')
    @require_api_key
    def get(self, genre_id):
        """Get playlists for a specific genre/mood"""
        try:
            playlists = ytmusic.get_genre_playlists(genre_id)
            return success_response({
                'playlists': playlists,
                'total': len(playlists)
            })
        except Exception as e:
            return error_response('GENRE_ERROR', str(e), 500)


# Keep Flask blueprint routes
@bp.route('/recommendations/<video_id>', methods=['GET'])
@require_api_key
def get_recommendations(video_id):
    limit = min(int(request.args.get('limit', 20)), 50)
    try:
        tracks = ytmusic.get_recommendations(video_id, limit=limit)
        return success_response({'tracks': tracks, 'total': len(tracks)})
    except Exception as e:
        return error_response('RECOMMENDATIONS_ERROR', str(e), 500)


@bp.route('/trending', methods=['GET'])
@require_api_key
def get_trending():
    region = request.args.get('region', 'US').upper()
    try:
        tracks = ytmusic.get_trending(region)
        return success_response({'tracks': tracks, 'total': len(tracks), 'region': region})
    except Exception as e:
        return error_response('TRENDING_ERROR', str(e), 500)


@bp.route('/genres', methods=['GET'])
@require_api_key
def get_genres():
    try:
        genres = ytmusic.get_genres()
        return success_response({'genres': genres, 'total': len(genres)})
    except Exception as e:
        return error_response('GENRES_ERROR', str(e), 500)


@bp.route('/genres/<genre_id>', methods=['GET'])
@require_api_key
def get_genre_playlists(genre_id):
    try:
        playlists = ytmusic.get_genre_playlists(genre_id)
        return success_response({'playlists': playlists, 'total': len(playlists)})
    except Exception as e:
        return error_response('GENRE_ERROR', str(e), 500)
