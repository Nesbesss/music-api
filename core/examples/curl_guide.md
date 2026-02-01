# Music API - Curl Guide

This guide shows how to interact with the API using `curl` from your terminal.

## 1. Authentication

### Register a new user
```bash
curl -X POST http://localhost:5001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "name": "My Name"
  }'
```

### Login (get Token)
```bash
# Returns a JWT token. Copy the "token" field from the response.
curl -X POST http://localhost:5001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

---

## 2. Dashboard Operations (Requires Token)

Replace `YOUR_TOKEN` with the JWT token from the login step.

### Generate an API Key
```bash
curl -X POST http://localhost:5001/api/v1/dashboard/keys \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Terminal Key",
    "rate_limit": 100
  }'
```
*Save the "key" from the response!*

---

## 3. Using the Music API (Requires API Key)

Replace `YOUR_API_KEY` with the key you just generated.

### Search for a Song
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
  "http://localhost:5001/api/v1/search?q=The+Weeknd"
```

### Get Track Info
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
  "http://localhost:5001/api/v1/track/dQw4w9WgXcQ"
```

### Get Recommendations
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
  "http://localhost:5001/api/v1/recommendations/dQw4w9WgXcQ"
```

### Stream Audio
```bash
# Stream Audio directly to a file
curl -H "X-API-Key: YOUR_API_KEY" \
  "http://localhost:5001/api/v1/tracks/stream/dQw4w9WgXcQ" \
  --output track.mp3
```

### Get Lyrics (with Whisper AI)
```bash
curl -X POST -H "X-API-Key: YOUR_API_KEY" \
  "http://localhost:5001/api/v1/lyrics/dQw4w9WgXcQ/transcribe"
```
