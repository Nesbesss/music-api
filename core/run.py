#!/usr/bin/env python3
"""
Music API - Entry Point
Run with: python run.py
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app

app = create_app()

# ANSI Colors
class c:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def print_banner(host, port):
    print(f"""
{c.PURPLE}{c.BOLD}
    ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ 
    ████╗  ██║██╔═══██╗██║   ██║██╔══██╗
    ██╔██╗ ██║██║   ██║██║   ██║███████║
    ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║
    ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║
    ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝{c.END}
{c.DIM}    Zero-Gate Music Streaming Engine{c.END}

{c.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.END}

{c.GREEN}●{c.END} {c.BOLD}Server{c.END}     {c.DIM}→{c.END}  http://{host}:{port}
{c.BLUE}●{c.END} {c.BOLD}Dashboard{c.END}  {c.DIM}→{c.END}  http://{host}:{port}/player/
{c.YELLOW}●{c.END} {c.BOLD}API Docs{c.END}   {c.DIM}→{c.END}  http://{host}:{port}/docs
{c.PURPLE}●{c.END} {c.BOLD}Health{c.END}     {c.DIM}→{c.END}  http://{host}:{port}/api/v1/health

{c.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.END}
{c.DIM}Press Ctrl+C to stop the server{c.END}
""")

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    
    print_banner(host, port)
    
    # Suppress default Flask startup message
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.WARNING)
    
    try:
        app.run(debug=debug, host=host, port=port, use_reloader=debug)
    except OSError as e:
        if 'Address already in use' in str(e):
            print(f"\n{c.RED}{c.BOLD}⚠ Port {port} is already in use!{c.END}")
            print(f"{c.DIM}Run: lsof -ti :{port} | xargs kill -9{c.END}\n")
            sys.exit(1)
        raise
