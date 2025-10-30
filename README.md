# 🔔 Bell Ringers - CS Warm-Up Generator

A community-driven computer science bell ringer generator with unique "Lock & Spin" mechanics. Built with Flask and powered by Google Gemini AI.

## Features

- **Lock & Spin Generator**: Interactive slot-machine style interface for generating bell ringers
- **Anonymous Handles**: No signup required - users get auto-generated handles
- **My Binder**: Private collection of saved bell ringers
- **The Feed**: Community-shared bell ringers with usage statistics
- **Admin Dashboard**: Content management and user activity analytics
- **Mobile-First Design**: Fully responsive with collapsing menus and mobile-optimized tables
- **Print-Optimized Views**: Clean, printable bell ringer pages

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3 (no SQLAlchemy)
- **AI**: Google Gemini API (gemini-2.0-flash-exp model)
- **Frontend**: Vanilla JavaScript, Mobile-First CSS
- **Deployment**: Designed for PythonAnywhere

## Local Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file or set these environment variables:

```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
export SECRET_KEY="your_secret_key_here"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD="your_secure_password"
```

### 3. Initialize Database

```bash
cd bellringers
python init_db.py
```

This will create the database and an admin user with the credentials from your environment variables.

### 4. Run the Application

```bash
python app.py
```

The app will be available at:
- Main app: `http://localhost:5000/bellringers/`
- Admin login: `http://localhost:5000/bellringers/admin/login`

## PythonAnywhere Deployment

### 1. Upload Files

Upload all files to your PythonAnywhere account via:
- Git clone
- File upload
- Or rsync

### 2. Set Up Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 bellringers
pip install -r requirements.txt
```

### 3. Configure Environment Variables

In PythonAnywhere web app settings, add:
- `GEMINI_API_KEY`
- `SECRET_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`

### 4. WSGI Configuration

Edit your WSGI configuration file (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/bellringers'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['GEMINI_API_KEY'] = 'your_api_key_here'
os.environ['SECRET_KEY'] = 'your_secret_key_here'
os.environ['ADMIN_USERNAME'] = 'admin'
os.environ['ADMIN_PASSWORD'] = 'your_password_here'

# Import the Flask app
from app import app as application
```

### 5. Initialize Database

From PythonAnywhere Bash console:

```bash
cd bellringers
python init_db.py
```

### 6. Reload Web App

Click "Reload" in the PythonAnywhere web app dashboard.

## Getting a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and set it as `GEMINI_API_KEY`

## Blueprint Structure

This application is built as a self-contained Flask blueprint with the URL prefix `/bellringers`. This means:
- All routes are prefixed with `/bellringers/`
- Templates and static files are organized in subdirectories to avoid conflicts
- The entire app can be registered alongside other blueprints in a larger Flask application

**Example integration:**
```python
from flask import Flask
from bellringers import create_blueprint

app = Flask(__name__)
app.config.from_object(Config)

# Register the bellringers blueprint
bellringers_bp = create_blueprint()
app.register_blueprint(bellringers_bp)

# You can register other blueprints here
# app.register_blueprint(other_blueprint)
```

## Admin Access

- **URL**: `/bellringers/admin/login`
- **Default Username**: `admin` (or from `ADMIN_USERNAME` env var)
- **Default Password**: Set via `ADMIN_PASSWORD` env var
- **IMPORTANT**: Change the default password after first login!

## Admin Features

- **Dashboard**: View user statistics, API usage, and activity metrics
- **Content Management**: Approve or delete published bell ringers
- **User Activity**: Track individual user's API requests, saves, and logins

## Project Structure

```
bellringers/
├── app.py                      # Simple test file (registers blueprint)
├── requirements.txt            # Python dependencies
├── bellringers/                # Blueprint package
│   ├── __init__.py            # Blueprint factory (create_blueprint)
│   ├── config.py              # Configuration settings
│   ├── database.py            # SQLite3 database functions
│   ├── init_db.py             # Database initialization script
│   ├── routes.py              # Main application routes (register_routes)
│   ├── admin_routes.py        # Admin routes (create_admin_blueprint)
│   ├── gemini_api.py          # Gemini API integration
│   ├── static/
│   │   └── bellringers/       # Blueprint-namespaced static files
│   │       ├── css/
│   │       │   └── style.css  # Mobile-first stylesheet
│   │       └── js/
│   │           └── app.js     # Frontend JavaScript
│   ├── templates/
│   │   └── bellringers/       # Blueprint-namespaced templates
│   │       ├── base.html      # Base template
│   │       ├── generator.html # Lock & Spin UI
│   │       ├── binder.html    # My Binder page
│   │       ├── feed.html      # The Feed page
│   │       ├── print.html     # Print-optimized view
│   │       └── admin/
│   │           ├── login.html     # Admin login
│   │           ├── dashboard.html # Admin dashboard
│   │           └── content.html   # Content management
│   └── bellringers.db         # SQLite database (created on init)
```

## Usage

### For Teachers

1. **Generate**: Use the Lock & Spin interface to create bell ringers
   - Lock any slots you want to keep
   - Spin to randomize unlocked slots
   - Generate with AI

2. **Save**: Add bell ringers to your private binder

3. **Publish**: Share your best bell ringers with the community (requires admin approval)

4. **Browse**: Explore The Feed to find bell ringers shared by others

5. **Print**: Every bell ringer has a print-optimized view

### For Admins

1. **Login**: Go to `/bellringers/admin/login`

2. **Dashboard**: View overall statistics and user activity

3. **Content Management**: Approve or delete published bell ringers

4. **Monitor**: Track API usage and user engagement

## Unique Mechanics

### Lock & Spin
- Three slots: Topic, Format, Constraint
- Lock the ones you want to keep
- Spin randomizes the rest
- Creates addictive discovery experience

### Anonymous Handles
- No signup required
- Auto-generated friendly handles (e.g., "clever-python-256")
- Stored in browser localStorage
- Privacy-first approach

### Community Quality Control
- "Used by X teachers" metric instead of likes
- Most-used bell ringers rise to the top
- Admin approval for quality control

## Security Notes

- Change default admin password immediately
- Keep `SECRET_KEY` and `GEMINI_API_KEY` secure
- Don't commit sensitive environment variables to git
- Use strong passwords for admin accounts

## License

This project is created for educational purposes.

## Support

For issues or questions, please refer to the concept document or contact the development team.
