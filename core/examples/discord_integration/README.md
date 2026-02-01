# 🤖 Discord Music Notifier Guide

This guide shows you how to set up a simple "Music Logger" that posts to your Discord server whenever you download a song.

## 1. Get a Discord Webhook URL
1. Open Discord and go to your server.
2. Right-click a text channel (e.g., `#logs`) -> **Edit Channel**.
3. Go to **Integrations** -> **Webhooks**.
4. Click **New Webhook**.
5. Copy the **Webhook URL**. It looks like:
   `https://discord.com/api/webhooks/123456789/abcdef...`

## 2. Run the Notifier
Run the included python script:

```bash
python music_logger.py
```

It will ask for:
1. Your **Music API Key** (get it from the Dashboard).
2. Your **Discord Webhook URL** (from step 1).

## 3. How it Works
The script acts as a wrapper. When you search or download using this tool:
1. It calls the Music API to get the song.
2. It immediately sends a POST request to Discord with the details.
