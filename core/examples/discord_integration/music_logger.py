import requests
import json
import sys
import os
import time

# Configuration
API_BASE = "http://localhost:5001/api/v1"

def send_discord_notification(webhook_url, title, description, color=0x00ff00):
    """Sends a standardized embed to Discord."""
    payload = {
        "username": "Music Bot",
        "embeds": [{
            "title": title,
            "description": description,
            "color": color,
            "footer": {"text": "Nova Music API Client"},
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        }]
    }
    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        print(f"[!] Failed to send Discord notification: {e}")

def main():
    print("🎵 music_logger.py - Download & Notify")
    print("---------------------------------------")
    
    # Inputs
    api_key = input("Enter your Music API Key: ").strip()
    webhook_url = input("Enter Discord Webhook URL: ").strip()
    
    if not api_key or not webhook_url:
        print("Both API Key and Webhook URL are required.")
        return

    while True:
        print("\n[1] Search & Download")
        print("[2] Exit")
        choice = input("Select: ")
        
        if choice == '2':
            break
            
        if choice == '1':
            query = input("Search query: ")
            
            # NOTIFY SEARCH
            send_discord_notification(
                webhook_url,
                "🔎 Search Performed",
                f"Query: **{query}**",
                color=0xf1c40f # Yellow
            )
            
            # 1. Search
            print(f"Searching for '{query}'...")
            try:
                res = requests.get(
                    f"{API_BASE}/search",
                    headers={"X-API-Key": api_key},
                    params={"q": query}
                )
                if res.status_code != 200:
                    print(f"Error: {res.text}")
                    continue
                    
                data = res.json()
                tracks_list = data.get('data', {}).get('tracks', [])
                
                if not tracks_list:
                    print("No results found.")
                    continue
                    
                # List results
                for i, t in enumerate(tracks_list[:5]):
                    artist_name = t['artists'][0]['name'] if t.get('artists') else "Unknown"
                    duration = t.get('duration_ms', 0) / 1000
                    print(f"{i+1}. {t['name']} - {artist_name} ({duration}s)")
                    
                # Select
                sel = input("Select track (1-5): ")
                try:
                    idx = int(sel) - 1
                    track = tracks_list[idx]
                except:
                    print("Invalid selection.")
                    continue

                # 2. Download
                track_title = track['name']
                artist_name = track['artists'][0]['name'] if track.get('artists') else "Unknown"
                duration_str = f"{track.get('duration_ms', 0)/1000}s"
                
                print(f"Downloading {track_title}...")
                
                # NOTIFY START
                send_discord_notification(
                    webhook_url,
                    "⬇️ Download Started",
                    f"**Track:** {track_title}\n**Artist:** {artist_name}",
                    color=0x3498db # Blue
                )

                stream_url = f"{API_BASE}/tracks/stream/{track['id']}"
                
                # Stream to file
                clean_title = "".join(c for c in track_title if c.isalnum() or c in (' ', '-', '_')).strip()
                filename = f"{clean_title}.mp3"
                
                with requests.get(stream_url, headers={"X-API-Key": api_key}, stream=True) as r:
                    if r.status_code == 200:
                        total_size = int(r.headers.get('content-length', 0))
                        
                        with open(filename, 'wb') as f:
                            if total_size == 0:
                                f.write(r.content)
                            else:
                                downloaded = 0
                                for chunk in r.iter_content(chunk_size=8192):
                                    f.write(chunk)
                                    downloaded += len(chunk)
                                    # Progress Bar
                                    done = int(50 * downloaded / total_size)
                                    sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {downloaded//1024} KB")
                                    sys.stdout.flush()
                                    
                        print(f"\nSaved to: {os.path.abspath(filename)}")
                        
                        # 3. NOTIFY COMPLETE
                        print("Sending Completion Notification...")
                        send_discord_notification(
                            webhook_url,
                            "✅ Download Details",
                            f"**Track:** {track_title}\n**Artist:** {artist_name}\n**Size:** {downloaded//1024} KB",
                            color=0x2ecc71 # Green
                        )
                        print("Done!")
                    else:
                        print(f"Download failed: {r.status_code} {r.text}")
                        send_discord_notification(
                            webhook_url,
                            "❌ Download Failed",
                            f"Status: {r.status_code}",
                            color=0xe74c3c # Red
                        )
                        
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
