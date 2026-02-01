"""
Lyrics routes with Swagger documentation.
"""
from flask import Blueprint
from flask_restx import Resource, fields

from app.routes import lyrics_ns as ns
from app.services import require_api_key, transcription
from app.middleware import success_response, error_response

bp = Blueprint('lyrics', __name__)


@ns.route('/<video_id>')
class Lyrics(Resource):
    @ns.doc('get_lyrics', security='apikey')
    @ns.response(200, 'Lyrics with sync data if available')
    @require_api_key
    def get(self, video_id):
        """Get lyrics for a track (returns cached or pending status)"""
        try:
            cached = transcription.get_cached_lyrics(video_id)
            
            if cached:
                return success_response(cached)
            
            return success_response({
                'lyrics': 'Lyrics not yet transcribed',
                'source': 'pending',
                'synced': False,
                'segments': [],
                'hint': 'Call POST /api/v1/lyrics/{video_id}/transcribe to start transcription'
            })
        except Exception as e:
            return error_response('LYRICS_ERROR', str(e), 500)


@ns.route('/<video_id>/transcribe')
class Transcribe(Resource):
    @ns.doc('transcribe_lyrics', security='apikey')
    @ns.response(200, 'Transcribed lyrics with timestamps')
    @ns.response(503, 'Transcription service unavailable')
    @require_api_key
    def post(self, video_id):
        """Transcribe lyrics using Whisper AI (takes 15-30 seconds)"""
        try:
            result = transcription.transcribe(video_id)
            return success_response(result)
        except RuntimeError as e:
            return error_response('TRANSCRIPTION_UNAVAILABLE', str(e), 503)
        except Exception as e:
            return error_response('TRANSCRIPTION_ERROR', str(e), 500)


# Keep Flask blueprint routes
@bp.route('/lyrics/<video_id>', methods=['GET'])
@require_api_key
def get_lyrics(video_id):
    try:
        cached = transcription.get_cached_lyrics(video_id)
        if cached:
            return success_response(cached)
        return success_response({
            'lyrics': 'Lyrics not yet transcribed', 'source': 'pending',
            'synced': False, 'segments': [],
            'hint': 'Call POST /api/v1/lyrics/{video_id}/transcribe to start transcription'
        })
    except Exception as e:
        return error_response('LYRICS_ERROR', str(e), 500)


@bp.route('/lyrics/<video_id>/transcribe', methods=['POST'])
@require_api_key
def transcribe_lyrics(video_id):
    try:
        result = transcription.transcribe(video_id)
        return success_response(result)
    except RuntimeError as e:
        return error_response('TRANSCRIPTION_UNAVAILABLE', str(e), 503)
    except Exception as e:
        return error_response('TRANSCRIPTION_ERROR', str(e), 500)
