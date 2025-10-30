"""
Simple test file for Bell Ringers Flask Blueprint
For deployment on PythonAnywhere, use this file or create a WSGI file
"""
from flask import Flask
import os

from bellringers import create_blueprint
from bellringers.config import Config


# Create Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure session cookies work properly
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_PATH'] = '/'  # Important: cookie must be available to entire domain
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Register the bellringers blueprint - all initialization happens here
bellringers_bp = create_blueprint()
app.register_blueprint(bellringers_bp)


if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists(os.path.join('bellringers', 'bellringers.db')):
        print("Initializing database...")
        from bellringers.init_db import setup_database
        setup_database()

    print("Bell Ringers app is running!")
    print("Access the app at: http://localhost:5000/bellringers/")
    print("Admin login at: http://localhost:5000/bellringers/admin/login")

    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
