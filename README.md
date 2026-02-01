# 🎵 Project Nova

A production-ready, local-first developer platform for streaming music from YouTube Music. Designed for developers who want to build their own music applications without friction.

## 🚀 Experience the "Zero-Gate"
Project Nova is built for local development. By default, it allows anonymous access, meaning you can integrate it into your apps instantly without needing API keys or payment.

## 📦 Project Structure
- **`core/`**: The lightweight Project Nova API engine.
- **`sdk/`**: The official Python SDK with 100% coverage.
- **`web/`**: The premium landing page and one-liner installer.

## 🛠 Installation

### The One-Liner
Run this command in your terminal to automatically detect your system and set up the Core API:
```bash
curl -sSL https://nesbes.me/install.sh | bash
```

### ⚡️ The Nova Manager (`novam`)
Nova is managed via the official `novam` utility. After installation, use these commands to control your engine:

- **`./novam player`**: Starts the engine and opens the **Nova Player** (Local UI).
- **`./novam api`**: Starts the core API in headless mode.
- **`./novam status`**: Checks if the engine is running and healthy.
- **`./novam update`**: Pulls the latest features and security updates.

### Manual Setup (Legacy)
1. Clone: `git clone https://github.com/Nesbesss/music-api.git`
2. Core: `cd core && pip install -r requirements.txt`
3. Run: `python run.py`

## 🎵 Nova Player
Nova now includes a built-in, glassmorphic music player served at `http://localhost:5001/player`. It features real-time search, instant streaming, and a starfield aesthetic matching our landing page.

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
