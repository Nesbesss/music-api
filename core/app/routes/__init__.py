"""
Routes package - Namespace registration for Swagger docs.
Core-only version.
"""
from flask_restx import Api, Namespace

# Create namespaces
search_ns = Namespace('search', description='Search operations')
tracks_ns = Namespace('tracks', description='Track streaming & info')
artists_ns = Namespace('artists', description='Artist information')
albums_ns = Namespace('albums', description='Album information')
browse_ns = Namespace('browse', description='Trending, genres, recommendations')
lyrics_ns = Namespace('lyrics', description='Lyrics & transcription')
playlists_ns = Namespace('playlists', description='Playlist management')
health_ns = Namespace('health', description='Health checks')

def register_namespaces(api: Api):
    """Register all namespaces with the API."""
    from . import search, tracks, artists, albums, browse, lyrics, playlists, health, player
    
    api.add_namespace(search_ns, path='/search')
    api.add_namespace(tracks_ns, path='/tracks')
    api.add_namespace(artists_ns, path='/artists')
    api.add_namespace(albums_ns, path='/albums')
    api.add_namespace(browse_ns, path='/browse')
    api.add_namespace(lyrics_ns, path='/lyrics')
    api.add_namespace(playlists_ns, path='/playlists')
    api.add_namespace(health_ns, path='/health')
    api.add_namespace(player.player_ns, path='/player-docs')

def register_blueprints(app):
    """Register all blueprints with the Flask app."""
    from . import search, tracks, artists, albums, browse, lyrics, playlists, health, player
    prefix = '/api/v1'
    
    app.register_blueprint(search.bp, url_prefix=prefix)
    app.register_blueprint(tracks.bp, url_prefix=prefix)
    app.register_blueprint(artists.bp, url_prefix=prefix)
    app.register_blueprint(albums.bp, url_prefix=prefix)
    app.register_blueprint(browse.bp, url_prefix=prefix)
    app.register_blueprint(lyrics.bp, url_prefix=prefix)
    app.register_blueprint(playlists.bp, url_prefix=prefix)
    app.register_blueprint(health.bp, url_prefix=prefix)
    app.register_blueprint(player.bp, url_prefix='/player')

    # Public routes (landing redirect etc)
    from . import public
    app.register_blueprint(public.bp)
