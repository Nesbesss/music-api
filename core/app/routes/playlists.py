"""
Playlist routes with Swagger documentation.
"""
import json
import hashlib
from pathlib import Path

from flask import Blueprint, request, current_app
from flask_restx import Resource, fields

from app.routes import playlists_ns as ns
from app.services import require_api_key
from app.middleware import success_response, error_response

bp = Blueprint('playlists', __name__)


# Models for Swagger
create_playlist_input = ns.model('CreatePlaylistInput', {
    'name': fields.String(required=True, description='Playlist name'),
    'description': fields.String(description='Playlist description'),
    'tracks': fields.List(fields.Raw, description='Array of track objects')
})

share_playlist_input = ns.model('SharePlaylistInput', {
    'id': fields.String(required=True, description='Playlist ID'),
    'name': fields.String(description='Playlist name'),
    'createdAt': fields.String(description='Creation timestamp'),
    'tracks': fields.List(fields.Raw, description='Array of track objects')
})


def get_share_dir() -> Path:
    share_dir = Path(current_app.root_path).parent / 'playlist_shares'
    share_dir.mkdir(exist_ok=True)
    return share_dir


@ns.route('')
class PlaylistCreate(Resource):
    @ns.doc('create_playlist', security='apikey')
    @ns.expect(create_playlist_input)
    @ns.response(200, 'Created playlist info')
    @require_api_key
    def post(self):
        """Create a new playlist"""
        data = request.json or {}
        name = data.get('name')
        
        if not name:
            return error_response('MISSING_NAME', 'Playlist name is required', 400)
        
        playlist_id = 'local_' + name.replace(' ', '_')
        
        return success_response({
            'id': playlist_id,
            'name': name,
            'description': data.get('description', ''),
            'tracks': data.get('tracks', [])
        })


@ns.route('/share')
class PlaylistShare(Resource):
    @ns.doc('create_share_link', security='apikey')
    @ns.expect(share_playlist_input)
    @ns.response(200, 'Share ID for the playlist')
    @require_api_key
    def post(self):
        """Create a shareable playlist link"""
        data = request.json or {}
        playlist_id = data.get('id')
        
        if not playlist_id:
            return error_response('MISSING_ID', 'Playlist ID is required', 400)
        
        share_id = hashlib.md5(f"{playlist_id}{data.get('createdAt', '')}".encode()).hexdigest()[:12]
        
        share_file = get_share_dir() / f'{share_id}.json'
        with open(share_file, 'w') as f:
            json.dump(data, f)
        
        return success_response({
            'shareId': share_id,
            'shareUrl': f"/playlist/{share_id}"
        })


@ns.route('/<share_id>')
class PlaylistGet(Resource):
    @ns.doc('get_shared_playlist')
    @ns.response(200, 'Playlist data')
    @ns.response(404, 'Playlist not found')
    def get(self, share_id):
        """Get a shared playlist by ID (no auth required)"""
        share_file = get_share_dir() / f'{share_id}.json'
        
        if not share_file.exists():
            return error_response('PLAYLIST_NOT_FOUND', 'Playlist not found', 404)
        
        with open(share_file, 'r') as f:
            playlist = json.load(f)
        
        return success_response(playlist)


# Keep Flask blueprint routes
@bp.route('/playlists', methods=['POST'])
@require_api_key
def create_playlist():
    data = request.json or {}
    name = data.get('name')
    if not name:
        return error_response('MISSING_NAME', 'Playlist name is required', 400)
    playlist_id = 'local_' + name.replace(' ', '_')
    return success_response({
        'id': playlist_id, 'name': name,
        'description': data.get('description', ''), 'tracks': data.get('tracks', [])
    })


@bp.route('/playlists/share', methods=['POST'])
@require_api_key
def create_share_link():
    data = request.json or {}
    playlist_id = data.get('id')
    if not playlist_id:
        return error_response('MISSING_ID', 'Playlist ID is required', 400)
    share_id = hashlib.md5(f"{playlist_id}{data.get('createdAt', '')}".encode()).hexdigest()[:12]
    share_file = get_share_dir() / f'{share_id}.json'
    with open(share_file, 'w') as f:
        json.dump(data, f)
    return success_response({'shareId': share_id, 'shareUrl': f"/playlist/{share_id}"})


@bp.route('/playlists/<share_id>', methods=['GET'])
def get_shared_playlist(share_id):
    share_file = get_share_dir() / f'{share_id}.json'
    if not share_file.exists():
        return error_response('PLAYLIST_NOT_FOUND', 'Playlist not found', 404)
    with open(share_file, 'r') as f:
        playlist = json.load(f)
    return success_response(playlist)
