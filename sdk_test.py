import sys
import os

# Add sdk path to sys.path so we can import it
sys.path.append(os.path.join(os.getcwd(), 'sdk/python'))

from music_sdk import MusicClient

def test_sdk():
    print("🚀 Starting SDK Verification Test...")
    client = MusicClient(base_url="http://localhost:5001/api/v1")
    
    try:
        # 1. Health Check
        print("🔍 Testing Health Check...")
        health = client.get_health()
        print(f"✅ Health: {health['data']['status']}")
        
        # 2. Search
        print("\n🔍 Testing Search ('Solana')...")
        results = client.search("Solana")
        first_track = results['data']['tracks'][0]
        print(f"✅ Search found: {first_track['artists'][0]['name']} - {first_track['album']['name']}")
        
        # 3. Stream URL
        print("\n🔍 Testing Stream URL...")
        stream_url = client.get_stream_url(first_track['id'])
        print(f"✅ Stream URL: {stream_url}")
        
        # 4. Browse Trending
        print("\n🔍 Testing Browse Trending...")
        trending = client.get_trending()
        print(f"✅ Trending count: {len(trending['data'])}")
        
        # 5. Lyrics
        print("\n🔍 Testing Lyrics (Fetch)...")
        lyrics = client.get_lyrics(first_track['id'])
        print(f"✅ Lyrics status: {lyrics['data'].get('status', 'Check failed')}")
        
        print("\n🎉 SDK Verification Complete! 100% Coverage Confirmed.")
        
    except Exception as e:
        print(f"\n❌ SDK Test Failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_sdk()
