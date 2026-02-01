from flask import Blueprint, render_template
from flask_restx import Namespace, Resource

# Blueprint for the UI
bp = Blueprint('player_ui', __name__)

# Namespace for documentation/metadata
player_ns = Namespace('player', description='Nova Music Player')

@bp.route('/')
def player_page():
    """Serve the Nova Player web UI"""
    return render_template('player.html')

@player_ns.route('/status')
class PlayerStatus(Resource):
    def get(self):
        """Check if the player subsystem is active"""
        return {'status': 'active', 'ui': '/player/'}
