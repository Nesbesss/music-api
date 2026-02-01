import requests
import time
import json

# Configuration
BASE_URL = "http://localhost:5001/api/v1"
EMAIL = "demo_user@example.com"
PASSWORD = "password123"
NAME = "Demo User"

def print_step(msg):
    print(f"\n{'='*50}\n{msg}\n{'='*50}")

def print_json(data):
    print(json.dumps(data, indent=2))

def main():
    session = requests.Session()

    # 1. Register or Login
    print_step("1. Authenticating...")
    
    # Try logging in first
    login_payload = {"email": EMAIL, "password": PASSWORD}
    response = session.post(f"{BASE_URL}/auth/login", json=login_payload)
    
    if response.status_code == 401:
        print("User not found, registering...")
        register_payload = {"email": EMAIL, "password": PASSWORD, "name": NAME}
        response = session.post(f"{BASE_URL}/auth/register", json=register_payload)
    
    if response.status_code not in [200, 201]:
        print(f"Authentication failed: {response.text}")
        return

    auth_data = response.json()['data']
    token = auth_data['token']
    print(f"Display Name: {auth_data['user']['name']}")
    print(f"Session Token: {token[:10]}...")

    # 2. Get or Create API Key
    print_step("2. Managing API Key...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # List keys
    keys_resp = session.get(f"{BASE_URL}/dashboard/keys", headers=headers)
    keys = keys_resp.json()['data']['keys']
    
    api_key = None
    if keys:
        print(f"Found {len(keys)} existing key(s).")
        if len(keys) >= 3:
            print("Max keys reached. Revoking the oldest key to make room...")
            oldest_key = sorted(keys, key=lambda k: k['created_at'])[0]
            session.delete(f"{BASE_URL}/dashboard/keys/{oldest_key['id']}", headers=headers)
        
        print("Creating a fresh key for this demo...")
    
    # Create new key
    create_payload = {"name": f"Demo Key {int(time.time())}", "rate_limit": 100}
    create_resp = session.post(f"{BASE_URL}/dashboard/keys", headers=headers, json=create_payload)
    
    if create_resp.status_code == 201:
        key_data = create_resp.json()['data']
        api_key = key_data['key']
        print(f"Created new API Key: {api_key}")
    else:
        print(f"Failed to create key: {create_resp.text}")
        return

    # 3. Use the API Key to Search
    print_step("3. Searching for Music...")
    search_headers = {"X-API-Key": api_key}
    
    # Search for "Daft Punk"
    query = "Daft Punk"
    search_resp = session.get(f"{BASE_URL}/search", params={"q": query}, headers=search_headers)
    
    if search_resp.status_code == 200:
        data = search_resp.json()['data']
        results = data.get('tracks', [])
        print(f"Found {len(results)} results for '{query}'")
        if results:
            first_track = results[0]
            print(f"Top Result: {first_track['name']} by {first_track['artists'][0]['name']}")
            video_id = first_track['id']
            
            # 4. Get Track Details & Stream
            print_step(f"4. Getting Details for {video_id}...")
            track_resp = session.get(f"{BASE_URL}/track/{video_id}", headers=search_headers)
            if track_resp.status_code == 200:
                print("Track Details received.")
                # We won't print full JSON to save space, but it's there
            
            # 5. Check Usage in Dashboard
            print_step("5. Checking Usage Stats...")
            # Wait a moment for async logging (if any)
            time.sleep(1)
            usage_resp = session.get(f"{BASE_URL}/dashboard/usage", headers=headers)
            usage_data = usage_resp.json()['data']
            print(f"Total Requests: {usage_data['total_requests']}")
            
    else:
        print(f"Search failed: {search_resp.text}")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running on http://localhost:5001?")
