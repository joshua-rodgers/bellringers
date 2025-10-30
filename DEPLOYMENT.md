# Bell Ringers - Deployment Checklist

## Pre-Deployment Checklist

- [ ] Get Google Gemini API key from https://makersuite.google.com/app/apikey
- [ ] Choose a strong SECRET_KEY for Flask sessions
- [ ] Set secure admin username and password
- [ ] Review and test all routes locally (optional)

## PythonAnywhere Deployment Steps

### 1. Upload Code

**Option A: Git Clone**
```bash
git clone <your-repo-url>
cd bellringers
```

**Option B: Manual Upload**
- Upload all files via PythonAnywhere file manager
- Maintain the directory structure

### 2. Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 bellringers
workon bellringers
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
cd bellringers
python init_db.py
```

This creates:
- SQLite database with all tables
- Default admin user

### 5. Configure WSGI File

Edit `/var/www/<username>_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

# Add project directory
project_home = '/home/<username>/bellringers'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['GEMINI_API_KEY'] = 'your_actual_api_key_here'
os.environ['SECRET_KEY'] = 'your_secure_random_string_here'
os.environ['ADMIN_USERNAME'] = 'admin'
os.environ['ADMIN_PASSWORD'] = 'your_secure_password_here'

# Import Flask app
from app import app as application
```

### 6. Configure Web App

In PythonAnywhere Web tab:

1. **Source code**: `/home/<username>/bellringers`
2. **Working directory**: `/home/<username>/bellringers`
3. **Virtualenv**: `/home/<username>/.virtualenvs/bellringers`

### 7. Reload Web App

Click the big green "Reload" button

### 8. Test the Application

Visit `https://<username>.pythonanywhere.com`

## Post-Deployment

### Test These Features

1. **Generator Page** (`/`)
   - [ ] Lock & Spin works
   - [ ] Generate creates bell ringers (requires valid GEMINI_API_KEY)
   - [ ] Save to binder works
   - [ ] Publish to feed works

2. **My Binder** (`/binder`)
   - [ ] Shows saved bell ringers
   - [ ] Print view works

3. **The Feed** (`/feed`)
   - [ ] Shows approved public bell ringers
   - [ ] Sorting works (New/Popular)
   - [ ] Add to binder works

4. **Admin** (`/admin/login`)
   - [ ] Login works with credentials
   - [ ] Dashboard shows statistics
   - [ ] Content management works
   - [ ] Approve/delete functions work

### Security Checklist

- [ ] Change default admin password immediately
- [ ] Verify GEMINI_API_KEY is set correctly
- [ ] Ensure SECRET_KEY is random and secure
- [ ] Test that anonymous handles are being generated
- [ ] Verify database file permissions are correct

## Troubleshooting

### Error: "No module named 'flask'"
**Solution**: Activate virtual environment and install requirements
```bash
workon bellringers
pip install -r requirements.txt
```

### Error: "Database not found"
**Solution**: Initialize the database
```bash
cd bellringers
python init_db.py
```

### Error: "GEMINI_API_KEY not set"
**Solution**: Add the environment variable to your WSGI file

### Error: 404 on all pages
**Solution**: Check the WSGI file configuration and reload the web app

### Error: Static files not loading
**Solution**: In PythonAnywhere Web tab, configure static files:
- URL: `/static/`
- Directory: `/home/<username>/bellringers/bellringers/static/`

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `GEMINI_API_KEY` | Google Gemini API authentication | `AIza...` |
| `SECRET_KEY` | Flask session security | `random-secure-string-123` |
| `ADMIN_USERNAME` | Admin login username | `admin` |
| `ADMIN_PASSWORD` | Admin login password | `SecurePass123!` |

## Database Location

The SQLite database is located at:
```
/home/<username>/bellringers/bellringers/bellringers.db
```

**Backup regularly!** Download via file manager or:
```bash
scp <username>@ssh.pythonanywhere.com:/home/<username>/bellringers/bellringers/bellringers.db ./backup.db
```

## Support

- Check application logs in PythonAnywhere
- Review error logs in the web app dashboard
- Ensure all environment variables are set correctly
- Verify database file exists and has write permissions

## Quick Links

- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Gemini API](https://ai.google.dev/)
