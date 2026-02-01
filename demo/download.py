#!/usr/bin/env python3
"""
Nova Music Downloader Demo
Downloads music using the Nova API.

Usage:
    python download.py "song name"
    python download.py "Starboy" --output ~/Music/
"""
import argparse
import requests
import os
import sys
from pathlib import Path

# Nova API Base URL
API_BASE = os.getenv("NOVA_API", "http://localhost:5001")

# ANSI Colors
class c:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def search_track(query: str, limit: int = 5):
    """Search for tracks using the Nova API."""
    print(f"{c.CYAN}🔍 Searching for:{c.END} {c.BOLD}{query}{c.END}")
    
    try:
        resp = requests.get(f"{API_BASE}/api/v1/search", params={"q": query, "limit": limit})
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", {}).get("tracks", [])
    except requests.RequestException as e:
        print(f"{c.RED}✖ API Error: {e}{c.END}")
        print(f"{c.DIM}Make sure the Nova API is running: ./novam api{c.END}")
        sys.exit(1)

def download_track(track_id: str, filename: str, output_dir: Path):
    """Download a track from the Nova API."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename
    
    print(f"{c.BLUE}⬇ Downloading...{c.END}")
    
    try:
        resp = requests.get(f"{API_BASE}/api/v1/tracks/stream/{track_id}", stream=True)
        resp.raise_for_status()
        
        total = int(resp.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = int((downloaded / total) * 50)
                    bar = f"{'█' * pct}{'░' * (50 - pct)}"
                    print(f"\r  {c.DIM}{bar}{c.END} {downloaded // 1024}KB", end='')
        
        print(f"\n{c.GREEN}✓ Saved:{c.END} {output_path}")
        return output_path
    except requests.RequestException as e:
        print(f"{c.RED}✖ Download failed: {e}{c.END}")
        sys.exit(1)

def sanitize_filename(name: str) -> str:
    """Remove invalid characters from filename."""
    invalid = '<>:"/\\|?*'
    for char in invalid:
        name = name.replace(char, '')
    return name.strip()

def main():
    parser = argparse.ArgumentParser(description="Download music using the Nova API")
    parser.add_argument("query", help="Song name or search query")
    parser.add_argument("-o", "--output", default="./downloads", help="Output directory")
    parser.add_argument("-n", "--number", type=int, default=1, help="Track number to download (1-5)")
    args = parser.parse_args()
    
    print(f"""
{c.PURPLE}{c.BOLD}╔══════════════════════════════════════╗
║      🎵 Nova Music Downloader        ║
╚══════════════════════════════════════╝{c.END}
""")
    
    # Search
    tracks = search_track(args.query)
    
    if not tracks:
        print(f"{c.YELLOW}No tracks found for '{args.query}'{c.END}")
        sys.exit(0)
    
    # Display results
    print(f"\n{c.CYAN}Found {len(tracks)} tracks:{c.END}\n")
    for i, track in enumerate(tracks[:5], 1):
        artist = track.get("artists", [{}])[0].get("name", "Unknown")
        name = track.get("name", "Unknown")
        print(f"  {c.BOLD}{i}.{c.END} {name} {c.DIM}by{c.END} {artist}")
    
    # Select track
    idx = min(args.number, len(tracks)) - 1
    selected = tracks[idx]
    
    # Build filename
    artist = selected.get("artists", [{}])[0].get("name", "Unknown")
    name = selected.get("name", "Unknown")
    filename = sanitize_filename(f"{artist} - {name}.m4a")
    
    print(f"\n{c.GREEN}Selected:{c.END} {c.BOLD}{name}{c.END} by {artist}\n")
    
    # Download
    download_track(selected["id"], filename, Path(args.output))
    
    print(f"\n{c.GREEN}{c.BOLD}✓ Done!{c.END}\n")

if __name__ == "__main__":
    main()
