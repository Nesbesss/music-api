import requests
import time
import sys

# Configuration
BASE_URL = "http://localhost:5001/api/v1"

def main():
    print("🛡️  Nova API Safety Feature Tester")
    print("==================================")
    
    # 1. Login
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ").strip()
    
    print("\nLogging in...")
    try:
        resp = requests.post(f"{BASE_URL}/auth/login", json={'email': email, 'password': password})
        if resp.status_code != 200:
            print(f"Login failed: {resp.text}")
            return
        token = resp.json()['data']['token']
        print("✅ Login success")
    except Exception as e:
        print(f"Connection error: {e}")
        return

    # 2. Webhook URL
    print("\n[Step 1] Setup Key Webhook")
    webhook_url = input("Enter Discord Webhook URL: ").strip()
    if not webhook_url: return

    # 3. Create Key
    key_name = f"Safety Test {int(time.time())}"
    print(f"Creating key '{key_name}' with webhook...")
    
    resp = requests.post(
        f"{BASE_URL}/dashboard/keys", 
        headers={'Authorization': f'Bearer {token}'},
        json={'name': key_name, 'alert_webhook_url': webhook_url}
    )
    
    if resp.status_code != 201:
        print(f"Failed to create key: {resp.text}")
        return

    data = resp.json()['data']['key']
    api_key = data['key'] # The raw key
    key_id = data['id']
    saved_webhook = data.get('alert_webhook_url')

    print(f"✅ Key Created!")
    print(f"   ID: {key_id}")
    print(f"   Name: {data['name']}")
    print(f"   Saved Webhook: {saved_webhook}")
    
    if saved_webhook == webhook_url:
        print("   -> PERSISTENCE CONFIRMED: Server returned the correct URL.")
    else:
        print("   -> WARNING: URL mismatch or not saved!")

    # 4. Trigger Usage
    print("\n[Step 2] Triggering Limit to Test Notification")
    print("Hit Enter to start downloading tracks until limit usage triggers...")
    input()
    
    confirm = input(f"This will consume downloads on key '{key_name}'. Continue? (y/n): ")
    if confirm.lower() != 'y': return

    # Search for short tracks
    print("Searching...")
    search_resp = requests.get(f"{BASE_URL}/search", params={'q': 'sound effects', 'limit': 5}, headers={'X-API-Key': api_key})
    tracks = search_resp.json().get('data', {}).get('tracks', [])
    
    if not tracks:
        print("No tracks found to download.")
        return

    print(f"Found {len(tracks)} tracks. Downloading...")
    
    for i, track in enumerate(tracks):
        print(f"Downloading {i+1}: {track['name']}...")
        start = time.time()
        # Stream just a bit to trigger logging
        with requests.get(f"{BASE_URL}/tracks/stream/{track['id']}", headers={'X-API-Key': api_key}, stream=True) as r:
            # Read 1 chunk
            for _ in r.iter_content(1024): break 
            
            if r.status_code == 200:
                print("   -> Success (200)")
            elif r.status_code == 429:
                print("   -> LIMIT REACHED (429)!")
                print("   🚨 Check your Discord now! You should see a notification with an Emergency Block link.")
                break
            else:
                print(f"   -> Failed: {r.status_code}")
                
        time.sleep(1)

    print("\n[Step 3] Verification")
    print("If you clicked the Emergency Block link in Discord:")
    input("Press Enter to check key status...")
    
    # Re-fetch key details
    print("Fetching key status...")
    detail_resp = requests.get(f"{BASE_URL}/dashboard/keys", headers={'Authorization': f'Bearer {token}'})
    keys = detail_resp.json()['data']['keys']
    this_key = next((k for k in keys if k['id'] == key_id), None)
    
    if this_key and this_key.get('is_blocked'):
        print(f"✅ Key IS BLOCKED!")
        print(f"   Reason: {this_key.get('block_reason')}")
    else:
        print("ℹ️ Key is NOT blocked. (Did you click the link?)")
        print(f"   Blocked Status: {this_key.get('is_blocked')}")

if __name__ == "__main__":
    main()
