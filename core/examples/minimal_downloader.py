import requests
import os
import sys

# Configuration
BASE_URL = "http://localhost:5001/api/v1"
DOWNLOAD_DIR = "downloads"

def main():
    print("\n" + "="*40)
    print("💎 NOVA REAL DOWNLOADER")
    print("="*40)
    print("This script performs a REAL download.")
    print("Server-side notifications will trigger automatically.")
    
    # Ensure download directory exists
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    
    # 1. API Key
    api_key = input("\nEnter your API Key: ").strip()
    if not api_key: return

    # 2. Search
    query = input("Search for a song: ")
    
    try:
        print(f"\n🔍 Searching for '{query}'...")
        res = requests.get(
            f"{BASE_URL}/search",
            headers={"X-API-Key": api_key},
            params={"q": query, "limit": 1}
        )
        
        if res.status_code != 200:
            print(f"❌ API Error: {res.text}")
            return
            
        tracks = res.json().get('data', {}).get('tracks', [])
        if not tracks:
            print("❌ No tracks found.")
            return
            
        track = tracks[0]
        artist_name = track['artists'][0]['name'] if isinstance(track['artists'][0], dict) else track['artists'][0]
        print(f"✅ Found: {track['name']} by {artist_name}")
        
        filename = f"{track['name']} - {artist_name}.mp3".replace("/", "_")
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        print(f"\n🚀 Downloading to: {filepath}...")
        
        with requests.get(
            f"{BASE_URL}/tracks/stream/{track['id']}", 
            headers={"X-API-Key": api_key}, 
            stream=True
        ) as r:
            if r.status_code == 200:
                total_size = int(r.headers.get('content-length', 0))
                downloaded = 0
                
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size:
                                done = int(50 * downloaded / total_size)
                                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {downloaded//1024}KB")
                                sys.stdout.flush()
                
                print(f"\n\n✨ Done! Saved to {filepath}")
            elif r.status_code == 429:
                print("\n⚠️  LIMIT REACHED! Server-side safety triggered.")
            else:
                print(f"\n❌ Server Error: {r.status_code}")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    print("\n" + "="*40)
    print("🔔 CHECK YOUR DISCORD!")
    print("The server just notified you for BOTH the search")
    print("and the download start. No webhook URL needed in script!")
    print("="*40)

if __name__ == "__main__":
    main()
