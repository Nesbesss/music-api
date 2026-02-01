import requests
from typing import Optional, List, Dict, Any

class MusicClient:
    """
    The official Python SDK for Music API.
    A complete wrapper for all API endpoints.
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "http://localhost:5001/api/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            self.headers["X-API-Key"] = self.api_key

    def _request(self, method: str, endpoint: str, params: dict = None, data: dict = None):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=data
        )
        response.raise_for_status()
        return response.json()

    # --- Search ---
    def search(self, query: str, filter_type: Optional[str] = None):
        """Search for songs, artists, and albums."""
        return self._request("GET", "/search", params={"q": query, "filter": filter_type})

    # --- Tracks ---
    def get_track(self, track_id: str):
        """Get detailed information about a track."""
        return self._request("GET", f"/tracks/{track_id}")

    def get_stream_url(self, track_id: str):
        """Get the direct streaming URL for a track."""
        return f"{self.base_url}/tracks/stream/{track_id}"

    # --- Artists ---
    def get_artist(self, artist_id: str):
        """Get artist info, top songs, and albums."""
        return self._request("GET", f"/artists/{artist_id}")

    # --- Albums ---
    def get_album(self, album_id: str):
        """Get album details with full track listing."""
        return self._request("GET", f"/albums/{album_id}")

    # --- Browse (Charts & Genres) ---
    def get_trending(self):
        """Get currently trending songs."""
        return self._request("GET", "/browse/trending")

    def get_genres(self):
        """List available genres and moods."""
        return self._request("GET", "/browse/genres")
        
    def get_genre_details(self, params: Dict[str, Any]):
        """Get detailed content for a specific genre/mood."""
        return self._request("GET", "/browse/genre", params=params)

    # --- Lyrics ---
    def get_lyrics(self, track_id: str):
        """Get lyrics for a track (cached or extracted)."""
        return self._request("GET", f"/lyrics/{track_id}")

    def transcribe_lyrics(self, track_id: str):
        """Trigger AI transcription for a track (Whisper)."""
        return self._request("POST", f"/lyrics/transcribe/{track_id}")

    # --- Playlists ---
    def create_playlist(self, name: str, description: str = "", tracks: List[Dict] = None):
        """Create a new playlist."""
        data = {
            "name": name,
            "description": description,
            "tracks": tracks or []
        }
        return self._request("POST", "/playlists", data=data)

    def share_playlist(self, playlist_data: Dict[str, Any]):
        """Create a share ID for a playlist."""
        return self._request("POST", "/playlists/share", data=playlist_data)

    def get_shared_playlist(self, share_id: str):
        """Retrieve a shared playlist by its share ID."""
        return self._request("GET", f"/playlists/{share_id}")

    # --- Tools ---
    def get_health(self):
        """Check API health and status."""
        return self._request("GET", "/health")
