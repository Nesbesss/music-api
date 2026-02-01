#!/bin/bash

# Music API - One-Liner Installer
# Distributed via nesbes.me

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🎵 Music API Installer${NC}"
echo -e "----------------------------------"

# 1. System Detection
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo -e "📍 System detected: ${GREEN}${MACHINE}${NC}"

# 2. Dependency Check (Python)
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}Error: python3 is not installed.${NC}"
    exit 1
fi

# 3. Download/Clone Core
echo -e "📦 Downloading Music API Core..."
if [ ! -d "core" ]; then
    git clone https://github.com/Nesbesss/music-api.git .
fi

# 4. Environment Setup
echo -e "⚙️ Setting up environment..."
if [ ! -f .env ]; then
    echo "FLASK_ENV=development" > .env
    echo "SECRET_KEY=$(openssl rand -hex 16)" >> .env
    echo "ALLOW_ANONYMOUS_ACCESS=true" >> .env
fi

# 5. Install Dependencies
echo -e "py 📥 Installing Python dependencies (this may take a minute)..."
pip3 install -r core/requirements.txt --quiet

echo -e "----------------------------------"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e ""
echo -e "To start your Music API Core:"
echo -e "  ${PURPLE}cd core && python3 run.py${NC}"
echo -e ""
echo -e "Documentation available at: ${GREEN}http://localhost:5001/docs${NC}"
echo -e "----------------------------------"
