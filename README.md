# 🎵 Music API Platform

A production-ready, local-first developer platform for streaming music from YouTube Music. Designed for developers who want to build their own music applications without friction.

## 🚀 Experience the "Zero-Gate"
Music API Core is built for local development. By default, it allows anonymous access, meaning you can integrate it into your apps instantly without needing API keys or payment.

## 📦 Project Structure
- **`core/`**: The lightweight REST API engine.
- **`sdk/`**: The official Python SDK with 100% coverage.
- **`web/`**: The premium landing page and one-liner installer.

## 🛠 Installation

### The One-Liner
Run this command in your terminal to automatically detect your system and set up the Core API:
```bash
curl -sSL https://nesbes.me/install.sh | bash
```

### Manual Setup
1. Clone the repository: `git clone https://github.com/Nesbesss/music-api.git`
2. Enter the core directory: `cd music-api/core`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `python run.py`

## 🧰 Python SDK
Get started in seconds with our official Python SDK:

```python
from music_sdk import MusicClient

# No API key needed for local core
client = MusicClient() 

# Search and Stream
results = client.search("Solana")
track = results['data']['tracks'][0]
stream_url = client.get_stream_url(track['id'])

print(f"Streaming: {track['name']} -> {stream_url}")
```

## 🌐 Landing Page
The landing page at [nesbes.me](https://nesbes.me) provides quick access to the installer and SDK documentation.

## 📄 License
MIT License - Build whatever you want. Created by [Nesbesss](https://github.com/Nesbesss).
