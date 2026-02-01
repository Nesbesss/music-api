"""
Public routes for API redirection and health.
Core-only version.
"""
from flask import Blueprint, redirect

bp = Blueprint('public', __name__)

@bp.route('/')
def index():
    """Redirect home to Swagger docs."""
    return redirect('/docs')

@bp.route('/health')
def health_redirect():
    """Redirect to v1 health."""
    return redirect('/api/v1/health')
