import requests
import time
import sys

# Configuration
BASE_URL = "http://localhost:5001/api/v1"

def main():
    print("🔔 Server-Side Notification Tester")
    print("==================================")
    print("This script tests if your API KEY sends notifications automatically.")
    print("You should NOT need to enter a webhook URL here (it should be set in the Dashboard).")
    
    # 1. Get Key
    api_key = input("\nEnter your API Key: ").strip()
    if not api_key: return

    # 2. Trigger Usage (Download)
    print("\nTriggering a download to test notification...")
    print("Searching for a test track...")
    
    try:
        # Search
        res = requests.get(
            f"{BASE_URL}/search",
            headers={"X-API-Key": api_key},
            params={"q": "notification test", "limit": 1}
        )
        
        if res.status_code != 200:
            print(f"❌ API Error: {res.text}")
            return
            
        data = res.json()
        tracks = data.get('data', {}).get('tracks', [])
        
        if not tracks:
            print("❌ No tracks found.")
            return
            
        track = tracks[0]
        print(f"Found: {track['name']} ({track['id']})")
        print("Downloading (simulated)...")
        
        # Stream
        start = time.time()
        with requests.get(f"{BASE_URL}/tracks/stream/{track['id']}", headers={"X-API-Key": api_key}, stream=True) as r:
            # Read a bit
            for _ in r.iter_content(4096): break
            
            if r.status_code == 200:
                print("✅ Download started successfully.")
            elif r.status_code == 429:
                print("⚠️  Limit Reached! (This should definitely trigger a webhook)")
            else:
                print(f"❌ Download failed: {r.status_code}")

    except Exception as e:
        print(f"Error: {e}")
        return

    print("\n------------------------------------------------")
    print("👉 NOW CHECK YOUR DISCORD!")
    print("------------------------------------------------")
    print("If you attached a Webhook to this API Key in the Dashboard,")
    print("you should see a notification there right now.")

if __name__ == "__main__":
    main()
