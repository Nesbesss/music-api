#!/usr/bin/env python3
"""
Music API - Entry Point
Run with: python run.py
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app

app = create_app()

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    🎵 Music API v1.0.0                       ║
╠══════════════════════════════════════════════════════════════╣
║  Server:  http://{host}:{port}                               ║
║  Docs:    http://{host}:{port}/docs                          ║
║  Health:  http://{host}:{port}/api/v1/health                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(debug=debug, host=host, port=port)
