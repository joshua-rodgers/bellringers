"""
Bell Ringers Flask Blueprint
A community-driven CS bell ringer generator with Lock & Spin mechanics
"""
from flask import Blueprint, session, request, jsonify


def create_blueprint():
    """
    Factory function to create and configure the bellringers blueprint.
    This should be called from the main app to register the blueprint.

    Returns:
        Blueprint: Configured bellringers blueprint with all routes and handlers
    """
    from . import database as db

    # Create the main blueprint with URL prefix
    bp = Blueprint(
        'bellringers',
        __name__,
        template_folder='templates',
        static_folder='static',
        url_prefix='/bellringers'
    )

    # Import and register main routes
    from .routes import register_routes
    register_routes(bp)

    # Import and register admin blueprint
    from .admin_routes import create_admin_blueprint
    admin_bp = create_admin_blueprint()
    bp.register_blueprint(admin_bp)

    # Register user registration endpoint
    @bp.route('/api/register', methods=['POST'])
    def register_user():
        """Register a new anonymous user handle"""
        data = request.get_json()
        handle = data.get('handle')

        if not handle:
            return jsonify({'error': 'No handle provided'}), 400

        # Create user if doesn't exist
        if not db.user_exists(handle):
            db.create_user(handle)

        # Set session
        session['user_handle'] = handle

        return jsonify({'success': True})

    # Register before_request handler
    @bp.before_request
    def check_session():
        """Ensure user session exists and update last active"""
        # Skip for static files and admin login
        if request.endpoint and ('static' in request.endpoint or 'admin.login' in request.endpoint):
            return

        # If user_handle in session, update last active
        if 'user_handle' in session:
            handle = session['user_handle']
            if db.user_exists(handle):
                db.update_last_active(handle)

    # Register context processor
    @bp.app_context_processor
    def inject_user():
        """Make user handle available in all templates"""
        return dict(user_handle=session.get('user_handle'))

    return bp
