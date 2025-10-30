"""
Main Flask application file for Bell Ringers
Designed for deployment on PythonAnywhere
"""
from flask import Flask, session, request, jsonify
import os
import sys

# Add the bellringers directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from bellringers import init_app
from bellringers.config import Config
from bellringers import database as db

# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
init_app(app)


@app.route('/api/register', methods=['POST'])
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


@app.before_request
def check_session():
    """Ensure user session exists"""
    # Skip for static files and admin login
    if request.endpoint and ('static' in request.endpoint or 'admin.login' in request.endpoint):
        return

    # If user_handle in session, update last active
    if 'user_handle' in session:
        handle = session['user_handle']
        if db.user_exists(handle):
            db.update_last_active(handle)


@app.context_processor
def inject_user():
    """Make user handle available in all templates"""
    return dict(user_handle=session.get('user_handle'))


@app.errorhandler(404)
def not_found(e):
    """Custom 404 page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>404 - Page Not Found</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background: #f8f9fa;
            }
            h1 { color: #4A90E2; }
            a {
                color: #4A90E2;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>🔔 Oops! Page not found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/">Go back to Bell Ringers</a>
    </body>
    </html>
    """, 404


@app.errorhandler(500)
def internal_error(e):
    """Custom 500 page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>500 - Server Error</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background: #f8f9fa;
            }
            h1 { color: #E74C3C; }
            a {
                color: #4A90E2;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>🔔 Something went wrong</h1>
        <p>We're experiencing technical difficulties. Please try again later.</p>
        <a href="/">Go back to Bell Ringers</a>
    </body>
    </html>
    """, 500


if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists(os.path.join('bellringers', 'bellringers.db')):
        print("Initializing database...")
        from bellringers.init_db import setup_database
        setup_database()

    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
