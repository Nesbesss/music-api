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
echo -e "� Welcome to Project Nova - The Zero-Gate Music Platform\n"

# 1. Check System Requirements
echo -e "🔍 Checking system for Nova requirements..."

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

# 2. Virtual Environment Setup
echo -e "🌐 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 3. Download/Clone Core
echo -e "📦 Downloading Nova Core..."
if [ ! -d "core" ]; then
    git clone https://github.com/Nesbesss/music-api.git .
fi

# 4. Environment Setup
echo -e "⚙️ Setting up Nova environment..."
if [ ! -f .env ]; then
    echo "FLASK_ENV=development" > .env
    echo "SECRET_KEY=$(openssl rand -hex 16)" >> .env
    echo "ALLOW_ANONYMOUS_ACCESS=True" >> .env
fi

# 5. Install Dependencies
echo -e " Installing dependencies (this may take a moment)..."
source venv/bin/activate
pip install -q -r core/requirements.txt

# 6. Finale
echo -e "\n✨ Nova is ready!"
echo -e "👉 To start, run: \033[1;36msource venv/bin/activate && python3 core/run.py\033[0m"
echo -e "📖 Documentation & Explorer: \033[4;36mhttps://nesbes.me\033[0m"
