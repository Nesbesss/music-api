from flask import Blueprint, send_from_directory, render_template, redirect, url_for
import os

bp = Blueprint('legacy_compat', __name__)

@bp.route('/api/search')
def legacy_search():
    from app.routes.search import search
    return search()

@bp.route('/api/track/<video_id>')
def legacy_track(video_id):
    from app.routes.tracks import get_track_legacy
    return get_track_legacy(video_id)

@bp.route('/api/stream/<video_id>')
def legacy_stream(video_id):
    return redirect(url_for('tracks.stream_track', video_id=video_id))

@bp.route('/api/health')
def legacy_health():
    from app.routes.health import health_check
    return health_check()

@bp.route('/api/recommendations/<video_id>')
def legacy_recommendations(video_id):
    from app.routes.browse import get_recommendations
    return get_recommendations(video_id)

@bp.route('/api/trending')
@bp.route('/api/browse/trending')
def legacy_trending():
    from app.routes.browse import get_trending
    return get_trending()

@bp.route('/api/playlist/<playlist_id>')
def legacy_get_playlist(playlist_id):
    from app.routes.playlists import get_playlist
    return get_playlist(playlist_id)

@bp.route('/api/playlist/create', methods=['POST'])
def legacy_create_playlist():
    from app.routes.playlists import create_playlist
    return create_playlist()

@bp.route('/api/set-token', methods=['POST'])
def legacy_set_token():
    from app.middleware import success_response
    return success_response({'status': 'token_set_ignored'})

@bp.route('/api/lyrics/<video_id>')
def legacy_lyrics(video_id):
    from app.routes.lyrics import get_lyrics
    return get_lyrics(video_id)

@bp.route('/api/lyrics/<video_id>/transcribe', methods=['POST'])
def legacy_transcribe(video_id):
    from app.routes.lyrics import transcribe_lyrics
    return transcribe_lyrics(video_id)

@bp.route('/api/create-playlist-share', methods=['POST'])
def legacy_create_playlist_share():
    from app.routes.playlists import create_share_link
    return create_share_link()
