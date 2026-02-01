"""
YouTube Music service wrapper.
"""
from typing import Optional, List, Dict, Any

from ytmusicapi import YTMusic
from flask import current_app
import yt_dlp
import threading
import requests

from .cache import cache


class YouTubeMusicService:
    """Wrapper for YouTube Music API."""
    
    _instance = None
    _ytmusic = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._ytmusic = YTMusic()
        return cls._instance
    
    def _get_thumbnail_url(self, video_id: str, thumbnails: list = None) -> str:
        """Get the best thumbnail URL for a video."""
        if video_id:
            return f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg'
        elif thumbnails:
            url = thumbnails[-1].get('url', '')
            if '=w' in url or '=s' in url:
                url = url.split('=w')[0].split('=s')[0]
            return url
        return ''
    
    def _format_track(self, track: Dict[str, Any]) -> Dict[str, Any]:
        """Format a track into consistent API response format."""
        video_id = track.get('videoId')
        thumbnail_url = self._get_thumbnail_url(video_id, track.get('thumbnails', []))
        
        return {
            'id': video_id,
            'name': track.get('title'),
            'artists': [{'name': artist['name'], 'id': artist.get('id')} 
                       for artist in track.get('artists', [])],
            'album': {
                'name': track.get('album', {}).get('name', 'Unknown Album') if track.get('album') else 'Unknown Album',
                'id': track.get('album', {}).get('id') if track.get('album') else None,
                'images': [{'url': thumbnail_url, 'height': 640, 'width': 640}]
            },
            'duration_ms': (track.get('duration_seconds') or 0) * 1000,
            'uri': f"ytmusic:{video_id}",
            'external_urls': {
                'youtube': f"https://music.youtube.com/watch?v={video_id}"
            }
        }
    
    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search for songs."""
        # Check cache first
        cache_key = f"search:{query}:{limit}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        results = self._ytmusic.search(query, filter='songs', limit=limit)
        formatted = [self._format_track(track) for track in results]
        
        # Cache for 5 minutes
        cache.set(cache_key, formatted, current_app.config.get('CACHE_TTL_SEARCH', 300))
        
        return formatted
    
    def get_recommendations(self, video_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get song recommendations based on a video."""
        cache_key = f"recommendations:{video_id}:{limit}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        watch_playlist = self._ytmusic.get_watch_playlist(videoId=video_id, limit=limit)
        
        if not watch_playlist or 'tracks' not in watch_playlist:
            return []
        
        tracks = []
        for track in watch_playlist['tracks']:
            track_id = track.get('videoId')
            if track_id and track_id != video_id:
                tracks.append(self._format_track(track))
        
        # Cache for 30 minutes
        cache.set(cache_key, tracks, current_app.config.get('CACHE_TTL_RECOMMENDATIONS', 1800))
        
        return tracks
    
    def get_artist(self, artist_id: str) -> Optional[Dict[str, Any]]:
        """Get artist information."""
        cache_key = f"artist:{artist_id}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        try:
            artist = self._ytmusic.get_artist(artist_id)
            
            result = {
                'id': artist_id,
                'name': artist.get('name'),
                'description': artist.get('description'),
                'subscribers': artist.get('subscribers'),
                'images': [{'url': thumb.get('url'), 'width': thumb.get('width'), 'height': thumb.get('height')} 
                          for thumb in artist.get('thumbnails', [])],
                'top_songs': [self._format_track(song) for song in artist.get('songs', {}).get('results', [])[:10]],
                'albums': [{
                    'id': album.get('browseId'),
                    'name': album.get('title'),
                    'year': album.get('year'),
                    'images': [{'url': thumb.get('url')} for thumb in album.get('thumbnails', [])]
                } for album in artist.get('albums', {}).get('results', [])[:10]]
            }
            
            # Cache for 1 hour
            cache.set(cache_key, result, current_app.config.get('CACHE_TTL_ARTIST', 3600))
            
            return result
        except Exception as e:
            current_app.logger.error(f"Error getting artist {artist_id}: {e}")
            return None
    
    def get_album(self, album_id: str) -> Optional[Dict[str, Any]]:
        """Get album information."""
        cache_key = f"album:{album_id}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        try:
            album = self._ytmusic.get_album(album_id)
            
            result = {
                'id': album_id,
                'name': album.get('title'),
                'artists': [{'name': artist.get('name'), 'id': artist.get('id')} 
                           for artist in album.get('artists', [])],
                'year': album.get('year'),
                'track_count': album.get('trackCount'),
                'duration': album.get('duration'),
                'images': [{'url': thumb.get('url'), 'width': thumb.get('width'), 'height': thumb.get('height')} 
                          for thumb in album.get('thumbnails', [])],
                'tracks': [self._format_track(track) for track in album.get('tracks', [])]
            }
            
            # Cache for 1 hour
            cache.set(cache_key, result, current_app.config.get('CACHE_TTL_ALBUM', 3600))
            
            return result
        except Exception as e:
            current_app.logger.error(f"Error getting album {album_id}: {e}")
            return None
    
    def get_trending(self, region: str = 'US') -> List[Dict[str, Any]]:
        """Get trending songs."""
        cache_key = f"trending:{region}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        try:
            # Get charts
            charts = self._ytmusic.get_charts(region)
            
            trending_tracks = []
            if charts and 'songs' in charts:
                items = charts['songs'].get('items', [])
                for item in items[:50]:
                    trending_tracks.append(self._format_track(item))
            
            # Cache for 30 minutes
            cache.set(cache_key, trending_tracks, 1800)
            
            return trending_tracks
        except Exception as e:
            current_app.logger.error(f"Error getting trending: {e}")
            return []
    
    def get_genres(self) -> List[Dict[str, Any]]:
        """Get available mood/genre categories."""
        cache_key = "genres"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        try:
            mood_categories = self._ytmusic.get_mood_categories()
            
            genres = []
            for category, playlists in mood_categories.items():
                for playlist in playlists:
                    genres.append({
                        'id': playlist.get('params'),
                        'name': playlist.get('title'),
                        'category': category
                    })
            
            # Cache for 24 hours
            cache.set(cache_key, genres, 86400)
            
            return genres
        except Exception as e:
            current_app.logger.error(f"Error getting genres: {e}")
            return []
    
    def get_genre_playlists(self, params: str) -> List[Dict[str, Any]]:
        """Get playlists for a mood/genre."""
        cache_key = f"genre_playlists:{params}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        try:
            playlists = self._ytmusic.get_mood_playlists(params)
            
            result = [{
                'id': p.get('playlistId'),
                'name': p.get('title'),
                'description': p.get('subtitle'),
                'images': [{'url': thumb.get('url')} for thumb in p.get('thumbnails', [])]
            } for p in playlists]
            
            # Cache for 1 hour
            cache.set(cache_key, result, 3600)
            
            return result
        except Exception as e:
            current_app.logger.error(f"Error getting genre playlists: {e}")
            return []
    def get_streaming_url(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get track streaming info using yt-dlp."""
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f'https://music.youtube.com/watch?v={video_id}', download=False)
                return {
                    'videoId': video_id,
                    'audioUrl': info.get('url'),
                    'title': info.get('title'),
                    'duration': info.get('duration')
                }
        except Exception as e:
            current_app.logger.error(f"Error getting streaming URL for {video_id}: {e}")
            return None

    # Thread-local storage for reuse
    _local = threading.local()

    def _get_resources(self):
        """Get thread-local YDL and Session to avoid re-init overhead."""
        if not hasattr(self._local, 'ydl'):
            # Pre-initialize YDL with fast options
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'skip_download': True,
                'force_ipv4': True,
                'extractor_args': {'youtube': {'player_client': ['android', 'ios']}},
            }
            self._local.ydl = yt_dlp.YoutubeDL(ydl_opts)
            
        if not hasattr(self._local, 'session'):
            # Persist TCP connections
            self._local.session = requests.Session()
            
        return self._local.ydl, self._local.session

    def stream_track(self, video_id: str, range_header: str = None):
        """Get a generator and headers for streaming directly from YouTube."""
        try:
            # Check cache for audio URL
            cache_key = f"stream_url:{video_id}"
            audio_url = cache.get(cache_key)
            
            ydl, session = self._get_resources()
            
            if not audio_url:
                # Use persistent YDL instance
                info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
                
                audio_url = info.get('url')
                if not audio_url:
                    if info.get('requested_formats'):
                        for fmt in info['requested_formats']:
                            if fmt.get('acodec') != 'none':
                                audio_url = fmt.get('url')
                                break
                    elif info.get('formats'):
                        for fmt in info['formats']:
                            if fmt.get('acodec') != 'none' and fmt.get('url'):
                                audio_url = fmt.get('url')
                                break
                
                if audio_url:
                    cache.set(cache_key, audio_url, 3600)
            
            if not audio_url:
                return None, None, 404
            
            upstream_headers = {}
            if range_header:
                upstream_headers['Range'] = range_header
            
            # Use persistent Session
            resp = session.get(audio_url, headers=upstream_headers, stream=True, timeout=30)
            
            content_type = resp.headers.get('Content-Type', 'audio/webm')
            response_headers = {
                'Content-Type': content_type,
                'Accept-Ranges': 'bytes',
            }
            
            status_code = resp.status_code
            if range_header and status_code == 206:
                response_headers['Content-Range'] = resp.headers.get('Content-Range')
                response_headers['Content-Length'] = resp.headers.get('Content-Length')
            else:
                if 'Content-Length' in resp.headers:
                    response_headers['Content-Length'] = resp.headers.get('Content-Length')
                status_code = 200
            
            def generate():
                try:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            yield chunk
                finally:
                    resp.close()
            
            return generate, response_headers, status_code
                
        except Exception as e:
            current_app.logger.error(f"Error streaming track {video_id}: {e}")
            return None, None, 500


# Singleton instance
ytmusic = YouTubeMusicService()
