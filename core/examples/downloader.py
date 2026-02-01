#!/usr/bin/env python3
"""
Simple Music Downloader using the Music API.
"""
import requests
import json
import sys
import os

# Configuration
API_URL = "http://localhost:5001/api/v1"

def clean_filename(title):
    return "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()

def main():
    print("🎵 Music API Downloader")
    print("=======================")
    
    # 1. Get API Key
    api_key = input("Enter your API Key: ").strip()
    if not api_key:
        print("API Key required!")
        return

    headers = {"X-API-Key": api_key}
    
    while True:
        try:
            print("\n--------------------------------")
            query = input("Search for a song (or 'q' to quit): ").strip()
            if query.lower() == 'q':
                break
            if not query:
                continue
                
            # 2. Search
            print(f"Searching for '{query}'...")
            resp = requests.get(f"{API_URL}/search", params={"q": query}, headers=headers)
            
            if resp.status_code == 403:
                print("Error: Invalid API Key or Rate Limit Exceeded.")
                return
            if resp.status_code != 200:
                print(f"Error: {resp.status_code} - {resp.text}")
                continue
                
            data = resp.json().get('data', {})
            results = data.get('tracks', []) if isinstance(data, dict) else []
            
            if not results:
                print("No results found.")
                continue
                
            # 3. List Results
            print("\nFound:")
            for i, track in enumerate(results[:5]):
                artist = track['artists'][0]['name'] if track['artists'] else "Unknown"
                print(f"{i+1}. {track['name']} - {artist} ({track.get('duration_ms', 0)/1000}s)")
                
            # 4. Select
            choice = input("\nEnter number to download (1-5) or 'c' to cancel: ").strip()
            if choice.lower() == 'c':
                continue
                
            try:
                idx = int(choice) - 1
                if idx < 0 or idx >= len(results[:5]):
                    print("Invalid selection.")
                    continue
            except ValueError:
                print("Invalid input.")
                continue
                
            track = results[idx]
            video_id = track['id']
            title = track['name']
            artist = track['artists'][0]['name'] if track['artists'] else "Unknown"
            filename = f"{clean_filename(artist)} - {clean_filename(title)}.mp3"
            
            # 5. Download
            stream_url = f"{API_URL}/tracks/stream/{video_id}"
            print(f"\nDownloading to '{filename}'...")
            
            download = requests.get(stream_url, headers=headers, stream=True)
            
            if download.status_code != 200:
                print(f"Failed to get stream: {download.status_code} - {download.text}")
                continue
                
            total_size = int(download.headers.get('content-length', 0))
            
            with open(filename, 'wb') as f:
                if total_size == 0:
                    f.write(download.content)
                else:
                    downloaded = 0
                    for data in download.iter_content(chunk_size=4096):
                        downloaded += len(data)
                        f.write(data)
                        done = int(50 * downloaded / total_size)
                        sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {downloaded//1024} KB")
                        sys.stdout.flush()
                        
            abs_path = os.path.abspath(filename)
            print(f"\nDownload complete! Saved to:\n{abs_path}")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
