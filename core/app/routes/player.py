from flask import Blueprint, send_from_directory, current_app
import os
from flask_restx import Namespace

bp = Blueprint('player', __name__)
player_ns = Namespace('player', description='Player UI metadata')

@bp.route('/')
@bp.route('/<path:path>')
def serve_player(path=""):
    """Serve the Improved Project Nova UI."""
    return send_from_directory(current_app.static_folder, 'index.html')
