# API Reference

The Music API is organized around REST. All requests should be made to `http://localhost:5001`.

## Base URL

```text
http://localhost:5001/api/v1
```

## Endpoints

### 🔍 Search

`GET /search`

Search for tracks, albums, or artists.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `q` | `string` | Yes | The search query. |

**Response**
```json
{
  "status": "success",
  "data": {
    "tracks": [...]
  }
}
```

---

### 🎵 Stream Audio

`GET /tracks/stream/{id}`

Get a direct audio stream for a specific track.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | `string` | Yes | The YouTube `videoId`. |

**Behavior**
Returns a `binary/octet-stream` (MP3).

---

### 📄 Track Info

`GET /track/{id}`

Get detailed metadata and lyrics for a specific track.

---

### 📈 Browse Trending

`GET /browse/trending`

Get the current top trending tracks.
