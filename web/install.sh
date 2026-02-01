#!/bin/bash

# Nova Core - One-Liner Installer
# Usage: curl -sSL https://nesbes.me/install.sh | bash

set -e

# Nova ASCII Art
echo -e "\033[1;34m"
echo "  _   _  ______      __      "
echo " | \ | |/ __ \ \    / /\     "
echo " |  \| | |  | \ \  / /  \    "
echo " | .   | |  | |\ \/ / /\ \   "
echo " | |\  | |__| | \  / ____ \  "
echo " |_| \_|\____/   \/_/    \_\ "
echo -e "\033[0m"
echo -e "🚀 Welcome to Project Nova - The Zero-Gate Music Platform\n"

# --- Legal Disclaimer ---
echo -e "\033[1;33m⚠️  IMPORTANT: Project Nova Legal Disclaimer\033[0m"
echo -e "This software is for personal study and educational purposes only."
echo -e "Usage of this tool for copyright-infringing activities is strictly prohibited."
echo -e "The developers are not responsible for any misuse or legal consequences."
echo -en "\n\033[1;36mDo you take full responsibility for your usage of Project Nova? (y/n): \033[0m"
read -n 1 -r < /dev/tty
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n🛑 Installation aborted. You must accept the terms to use Nova."
    exit 1
fi

# 1. Check System Requirements
echo -e "\n🔍 Checking system for Nova requirements..."

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo -e "❌ Python3 is not installed. Please install it first."
    exit 1
fi

# Check Git
if ! command -v git &> /dev/null; then
    echo -e "❌ Git is not installed. Please install it first."
    exit 1
fi

# 2. Download / Init project
echo -e "📦 Initializing Nova Environment..."
if [ ! -d ".git" ]; then
    if [ -z "$(ls -A 2>/dev/null)" ]; then
        git clone https://github.com/Nesbesss/music-api.git .
    else
        echo "⚠️  Directory is not empty. Synchronizing Nova into current path..."
        git init -q
        git remote add origin https://github.com/Nesbesss/music-api.git || git remote set-url origin https://github.com/Nesbesss/music-api.git
        git fetch -q --all
        git checkout -f main -q
    fi
else
    echo "♻️  Directory already exists. Syncing latest Nova features..."
    git pull origin main -q || echo "⚠️  Already up to date."
fi

# 3. Virtual Environment Setup
echo -e "🌐 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 4. Environment Setup
echo -e "⚙️  Configuring Nova..."
if [ ! -f .env ]; then
    echo "FLASK_ENV=development" > .env
    echo "SECRET_KEY=$(openssl rand -hex 16)" >> .env
    echo "ALLOW_ANONYMOUS_ACCESS=True" >> .env
fi

# 5. Install Dependencies
echo -e "📦 Installing dependencies (this may take a moment)..."
source venv/bin/activate
pip install -q -r core/requirements.txt

# 6. CLI Tool Setup
chmod +x novam
# Optional: could symlink here, but for now we instruct the user

# 7. Finale
echo -e "\n✨ \033[1;32mNova is ready!\033[0m"
echo -e "----------------------------------------"
echo -e "Project Nova is now managed via the \033[1;34mnovam\033[0m command."
echo -e "\n👉 \033[1;36m./novam player\033[0m  - Search & Stream music instantly"
echo -e "👉 \033[1;36m./novam api\033[0m     - Start the core engine"
echo -e "👉 \033[1;36m./novam status\033[0m  - Check engine health"
echo -e "----------------------------------------"

echo -en "\n🚀 \033[1;35mWould you like to open Nova Player right now? (y/n): \033[0m"
read -n 1 -r < /dev/tty
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./novam player
fi
