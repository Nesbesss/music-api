import yt_dlp
import sys

def test_stream(video_id):
    print(f"Testing stream extraction for {video_id}...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False, # Show output
        'extractor_args': {'youtube': {'player_client': ['android']}}
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
            url = info.get('url')
            print(f"URL: {url}")
            if not url:
                print("No URL found in main info.")
                # Check formats
                formats = info.get('formats', [])
                print(f"Formats count: {len(formats)}")
                for f in formats:
                    print(f" - {f.get('format_id')}: {f.get('acodec')} ({f.get('url') is not None})")
            return url
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else "dQw4w9WgXcQ"
    test_stream(vid)
