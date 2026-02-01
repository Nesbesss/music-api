"""
Track routes with Swagger documentation.
"""
from flask import Blueprint, request, Response, g
from flask_restx import Resource, fields
import yt_dlp
import requests as http_requests

from app.routes import tracks_ns as ns
from app.services import require_api_key
from app.middleware import success_response, error_response

bp = Blueprint('tracks', __name__)

from app.services.youtube_music import ytmusic

@ns.route('/<video_id>')
class Track(Resource):
    @ns.doc('get_track', security='apikey')
    @ns.response(200, 'Track info with audio URL')
    @ns.response(401, 'API key required')
    @require_api_key
    def get(self, video_id):
        """Get track info and streaming URL"""
        info = ytmusic.get_streaming_url(video_id)
        if info:
            info['thumbnail'] = f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg'
            return success_response(info)
        return error_response('TRACK_ERROR', 'Could not get track info', 500)


@bp.route('/tracks/stream/<video_id>', methods=['GET'])
@require_api_key
def stream_track(video_id):
    """Stream audio directly."""

    range_header = request.headers.get('Range')
    generate, headers, status = ytmusic.stream_track(video_id, range_header)
    
    if not generate:
        return error_response('STREAM_ERROR', 'Could not start stream', status)
        
    # Wrap generator for kill-switch
    from flask import current_app
    flask_app = current_app._get_current_object()
    def wrapped_generate():
        for chunk in generate():
            yield chunk
    
    return Response(wrapped_generate(), status=status, headers=headers)


@ns.route('/thumbnail/<video_id>')
class Thumbnail(Resource):
    @ns.doc('get_thumbnail')
    @ns.response(200, 'Thumbnail URL')
    def get(self, video_id):
        """Get the best available thumbnail for a video"""
        # We can still keep this here or move it to service
        qualities = ['maxresdefault', 'sddefault', 'hqdefault', 'mqdefault', 'default']
        for quality in qualities:
            thumbnail_url = f'https://i.ytimg.com/vi/{video_id}/{quality}.jpg'
            try:
                resp = http_requests.head(thumbnail_url, timeout=5)
                if resp.status_code == 200:
                    return success_response({'thumbnail_url': thumbnail_url})
            except:
                continue
        return success_response({'thumbnail_url': f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg'})

# ... existing blueprint routes ...
@bp.route('/track/<video_id>', methods=['GET'])
@require_api_key
def get_track_legacy(video_id):
    info = ytmusic.get_streaming_url(video_id)
    if info:
        info['thumbnail'] = f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg'
        return success_response(info)
    return error_response('TRACK_ERROR', 'Error', 500)

@bp.route('/thumbnail/<video_id>', methods=['GET'])
def get_thumbnail_legacy(video_id):
    return success_response({'thumbnail_url': f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg'})
