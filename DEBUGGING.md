# Debugging Guide for Bell Ringers App

## Common Issues and Solutions

### Issue 1: "No user session" error

**Symptoms:**
- "No user session" message on /bellringers/binder
- 401 Unauthorized when trying to generate

**Cause:**
The session isn't being set when you first visit the page.

**Solutions:**

1. **Check browser console for errors:**
   - Open Developer Tools (F12)
   - Go to Console tab
   - Look for any JavaScript errors
   - Check if the `/bellringers/api/register` call is succeeding

2. **Check cookies:**
   - Open Developer Tools (F12)
   - Go to Application/Storage tab
   - Look for a session cookie from your domain
   - If no cookie, sessions aren't working

3. **Verify SECRET_KEY is set:**
   ```bash
   # In Python console
   from app import app
   print(app.config['SECRET_KEY'])
   ```
   - Should NOT be empty
   - Should be a random string

4. **Clear browser data and try again:**
   - Clear cookies and local storage
   - Reload the page
   - Check if registration happens

5. **Manual test:**
   - Open browser console
   - Run: `localStorage.clear()`
   - Reload the page
   - Check console for registration request

### Issue 2: 404 on admin dashboard

**Symptoms:**
- 404 error when accessing `/bellringers/admin/dashboard`

**Solutions:**

1. **Verify the correct URL:**
   - Should be: `http://localhost:5000/bellringers/admin/login`
   - NOT: `http://localhost:5000/admin/login`

2. **Check if blueprint is registered:**
   ```python
   # In Python console
   from app import app
   for rule in app.url_map.iter_rules():
       if 'admin' in rule.rule:
           print(rule.rule, rule.endpoint)
   ```

3. **Restart the Flask app:**
   ```bash
   # Stop the app (Ctrl+C)
   # Start again
   python app.py
   ```

4. **Check for Python errors:**
   - Look at the terminal where Flask is running
   - Check for any import errors or exceptions

### Issue 3: Database not initialized

**Symptoms:**
- Errors about missing tables
- "no such table" errors

**Solution:**
```bash
cd bellringers
python init_db.py
```

### Testing Checklist

Run through these steps to verify everything works:

1. **Start the app:**
   ```bash
   python app.py
   ```

2. **Test main page:**
   - Visit: `http://localhost:5000/bellringers/`
   - Should see the generator page
   - Check browser console for errors

3. **Test session registration:**
   - Open browser Developer Tools
   - Go to Network tab
   - Reload the page
   - Look for POST to `/bellringers/api/register`
   - Should return 200 OK
   - Check Response tab for `{"success": true}`

4. **Test My Binder:**
   - Visit: `http://localhost:5000/bellringers/binder`
   - Should NOT show "No user session" error
   - Should show empty binder or your saved items

5. **Test generate (requires Gemini API key):**
   - Go to generator page
   - Select topic, format, constraint
   - Click "Generate"
   - Should NOT get 401 error
   - Should get a generated bell ringer (if API key is set)

6. **Test admin login:**
   - Visit: `http://localhost:5000/bellringers/admin/login`
   - Enter username: `admin`
   - Enter password: `changeme123` (or your configured password)
   - Should redirect to dashboard

7. **Test admin dashboard:**
   - After logging in
   - Should see statistics
   - Should NOT get 404

## Quick Fixes

### Reset everything:
```bash
# Stop the app
# Delete database
rm bellringers/bellringers.db

# Reinitialize
cd bellringers
python init_db.py
cd ..

# Restart app
python app.py
```

### Check session is working:
Add this to test sessions:
```python
# In app.py, add this route temporarily:
@app.route('/test-session')
def test_session():
    from flask import session
    session['test'] = 'it works!'
    return 'Session set'

@app.route('/check-session')
def check_session():
    from flask import session
    return f"Session: {session.get('test', 'not set')}"
```

Visit `/test-session` then `/check-session` - should see "Session: it works!"

## Environment Variables

Make sure these are set:

```bash
export SECRET_KEY="your-secret-key-here"
export GEMINI_API_KEY="your-gemini-key-here"
export ADMIN_USERNAME="admin"
export ADMIN_PASSWORD="changeme123"
```

Or create a `.env` file (NOT included in git):
```
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=changeme123
```

## Getting More Debug Information

### Enable Flask debug mode:
Already enabled in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Add logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check what routes are registered:
```python
from app import app
print("\n=== All Routes ===")
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint:50s} {rule.rule}")
```

## Still Having Issues?

1. Check that all files were updated correctly after refactoring
2. Make sure you're accessing URLs with `/bellringers/` prefix
3. Verify Flask and dependencies are installed: `pip install -r requirements.txt`
4. Check browser is not caching old JavaScript - hard refresh (Ctrl+Shift+R)
5. Try in incognito/private browsing mode to rule out cookie issues
