# Getting Started

Follow these steps to get your first music stream running with the Music API.

## 1. Authentication

All requests to the Music API require an API Key. You can generate one in the [Developer Dashboard](http://localhost:5002/dashboard/keys).

Include your key in the `X-API-Key` header:

```bash
X-API-Key: your_api_key_here
```

## 2. Your First Search

Search for your favorite artist or track:

```bash
curl -X GET "http://localhost:5001/api/v1/search?q=daft+punk" \
     -H "X-API-Key: YOUR_API_KEY"
```

## 3. Streaming Audio

To stream audio, use the `videoId` from the search result:

```bash
# This will stream the audio directly to your terminal (or a file)
curl -L "http://localhost:5001/api/v1/tracks/stream/videoId" \
     -H "X-API-Key: YOUR_API_KEY" \
     --output song.mp3
```

## 🔒 Security Tiers

- **Free Tier**: 25 downloads per week.
- **Enterprise**: Custom limits and dedicated support.
