"""
Transcription service using Whisper AI.
"""
import json
from pathlib import Path
from typing import Optional, Dict, Any

import yt_dlp
from flask import current_app


class TranscriptionService:
    """Service for transcribing audio using Whisper AI."""
    
    _instance = None
    _whisper_model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def _get_whisper_model(self):
        """Lazy load Whisper model."""
        if self._whisper_model is None:
            try:
                from faster_whisper import WhisperModel
                model_name = current_app.config.get('WHISPER_MODEL', 'base')
                device = current_app.config.get('WHISPER_DEVICE', 'cpu')
                compute_type = current_app.config.get('WHISPER_COMPUTE_TYPE', 'int8')
                current_app.logger.info(f"Loading Whisper model ({model_name}) on {device} with {compute_type}...")
                self._whisper_model = WhisperModel(model_name, device=device, compute_type=compute_type)
                current_app.logger.info("✓ Whisper model loaded!")
            except Exception as e:
                current_app.logger.error(f"Error loading Whisper model: {e}")
        return self._whisper_model
    
    def _get_cache_dir(self) -> Path:
        """Get the lyrics cache directory."""
        return current_app.config.get('LYRICS_CACHE_DIR', Path('/tmp/lyrics_cache'))
    
    def get_cached_lyrics(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get cached lyrics if available."""
        cache_file = self._get_cache_dir() / f"{video_id}.json"
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def transcribe(self, video_id: str) -> Dict[str, Any]:
        """Transcribe a video's audio using Whisper AI."""
        # Check cache first
        cached = self.get_cached_lyrics(video_id)
        if cached and cached.get('source') == 'whisper_ai':
            return cached
        
        cache_dir = self._get_cache_dir()
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        audio_file = cache_dir / f"{video_id}.mp3"
        
        # Download audio if not cached
        if not audio_file.exists():
            current_app.logger.info(f"📥 Downloading audio for {video_id}...")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(audio_file.with_suffix('')),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'https://music.youtube.com/watch?v={video_id}'])
        
        # Transcribe
        current_app.logger.info(f"🎵 Transcribing {video_id}...")
        model = self._get_whisper_model()
        
        if model is None:
            raise RuntimeError("Whisper model not available")
        
        segments_list, info = model.transcribe(str(audio_file), word_timestamps=False)
        
        lyrics_segments = []
        lyrics_lines = []
        
        for segment in segments_list:
            text = segment.text.strip()
            if text:
                lyrics_lines.append(text)
                lyrics_segments.append({
                    'start': segment.start,
                    'text': text
                })
        
        result = {
            'lyrics': '\n'.join(lyrics_lines),
            'source': 'whisper_ai',
            'synced': True,
            'language': info.language,
            'segments': lyrics_segments
        }
        
        # Cache result
        cache_file = cache_dir / f"{video_id}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        # Clean up audio file
        audio_file.unlink(missing_ok=True)
        
        current_app.logger.info(f"✓ Transcription complete: {len(lyrics_segments)} segments")
        
        return result


# Singleton instance
transcription = TranscriptionService()
