# Session Troubleshooting Guide

## Quick Test Steps

### 1. Stop and Restart the Flask App
```bash
# Press Ctrl+C to stop
# Then restart:
python app.py
```

### 2. Clear Browser Data
- Open Developer Tools (F12)
- Go to Application → Storage
- Clear all site data for localhost
- Or use Incognito/Private mode

### 3. Test Session Creation

**Step A: Visit the homepage**
```
http://localhost:5000/bellringers/
```

**Step B: Open Developer Console (F12)**
You should see:
```
Registering new user: clever-python-123  (or similar)
Registration response: {success: true, handle: "clever-python-123"}
```

**Step C: Check Network Tab**
- Look for POST request to `/bellringers/api/register`
- Status should be 200 OK
- Response should be `{"success": true, "handle": "..."}`

**Step D: Check Cookies**
- Open Application → Cookies → http://localhost:5000
- Should see a cookie named "session"
- Path should be "/"
- Value should be a long encrypted string

**Step E: Test Session Endpoint**
Visit:
```
http://localhost:5000/bellringers/api/debug/session
```

Should return:
```json
{
  "session_data": {"user_handle": "clever-python-123"},
  "user_handle": "clever-python-123",
  "has_session": true
}
```

**Step F: Test My Binder**
Visit:
```
http://localhost:5000/bellringers/binder
```

Should NOT show "No user session" error.

### 4. Check Terminal Output

In the terminal where Flask is running, you should see:
```
Session set for user: clever-python-123
Session contents: {'user_handle': 'clever-python-123'}
Binder page - Session data: {'user_handle': 'clever-python-123'}
```

## If Still Not Working

### Check 1: SECRET_KEY is set
```bash
# In the terminal where you run the app
echo $SECRET_KEY

# Or check in Python
python -c "from bellringers.config import Config; print(Config.SECRET_KEY)"
```

Should NOT be empty.

### Check 2: Cookie Settings
If using HTTPS (production), set:
```python
app.config['SESSION_COOKIE_SECURE'] = True
```

If using HTTP (development), set:
```python
app.config['SESSION_COOKIE_SECURE'] = False
```

### Check 3: Browser Console Errors
Look for:
- CORS errors
- Network errors
- JavaScript errors

### Check 4: Clear localStorage
In browser console:
```javascript
localStorage.clear()
location.reload()
```

## What Changed

1. **Session is now permanent**: `session.permanent = True`
2. **Session is explicitly modified**: `session.modified = True`
3. **Cookie path is set to root**: `SESSION_COOKIE_PATH = '/'`
4. **Registration is awaited**: Page waits for registration to complete
5. **Debug logging added**: Can see what's happening in terminal
6. **Debug endpoint added**: Can check session state at any time

## Manual Test

If automatic registration isn't working, test manually:

**1. Register manually:**
```bash
curl -X POST http://localhost:5000/bellringers/api/register \
  -H "Content-Type: application/json" \
  -d '{"handle": "test-user-123"}' \
  -c cookies.txt \
  -v
```

Look for `Set-Cookie: session=...` in the response headers.

**2. Use the cookie:**
```bash
curl http://localhost:5000/bellringers/api/debug/session \
  -b cookies.txt \
  -v
```

Should return the session data with the handle.

## Common Issues

### Issue: No session cookie in browser
**Cause**: SECRET_KEY not set or session not being created
**Fix**: Check SECRET_KEY, restart Flask app

### Issue: Cookie exists but not sent with requests
**Cause**: Cookie path mismatch or SameSite restriction
**Fix**: Ensure `SESSION_COOKIE_PATH = '/'` is set

### Issue: Registration happens but session lost on next page
**Cause**: Session not marked as permanent
**Fix**: Already fixed with `session.permanent = True`

### Issue: 401 Unauthorized on generate
**Cause**: Session cookie not included in fetch request
**Fix**: Already fixed with `credentials: 'include'`
