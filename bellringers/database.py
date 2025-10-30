"""
Database module for Bell Ringers app using SQLite3
"""
import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), 'bellringers.db')


@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH, timeout=10.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_db():
    """Initialize the database with all required tables"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Users table (anonymous handles)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                handle TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Bell ringers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bell_ringers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_handle TEXT NOT NULL,
                topic TEXT NOT NULL,
                format TEXT NOT NULL,
                constraint_type TEXT NOT NULL,
                content TEXT NOT NULL,
                is_public BOOLEAN DEFAULT 0,
                is_approved BOOLEAN DEFAULT 0,
                binder_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_handle) REFERENCES users(handle)
            )
        ''')

        # Activity logs table for statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_handle TEXT NOT NULL,
                action_type TEXT NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_handle) REFERENCES users(handle)
            )
        ''')

        # Admin users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Binder associations (who saved what)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS binder_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_handle TEXT NOT NULL,
                bell_ringer_id INTEGER NOT NULL,
                original_id INTEGER,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_handle) REFERENCES users(handle),
                FOREIGN KEY (bell_ringer_id) REFERENCES bell_ringers(id),
                UNIQUE(user_handle, bell_ringer_id)
            )
        ''')

        conn.commit()


def create_user(handle):
    """Create a new user with anonymous handle"""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (handle) VALUES (?)', (handle,))
            log_activity(handle, 'user_created', 'New user registered', cursor=cursor)
            return True
        except sqlite3.IntegrityError:
            return False


def user_exists(handle):
    """Check if a user exists"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE handle = ?', (handle,))
        return cursor.fetchone() is not None


def update_last_active(handle):
    """Update user's last active timestamp"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE handle = ?',
            (handle,)
        )


def save_bell_ringer(owner_handle, topic, format_type, constraint, content, is_public=False):
    """Save a bell ringer to the database"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bell_ringers
            (owner_handle, topic, format, constraint_type, content, is_public, is_approved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (owner_handle, topic, format_type, constraint, content, is_public, 0 if is_public else 1))

        bell_ringer_id = cursor.lastrowid

        # Add to user's binder
        cursor.execute('''
            INSERT INTO binder_items (user_handle, bell_ringer_id)
            VALUES (?, ?)
        ''', (owner_handle, bell_ringer_id))

        action_type = 'publish' if is_public else 'save'
        log_activity(owner_handle, action_type, f'Bell ringer created: {topic} - {format_type}', cursor=cursor)

        return bell_ringer_id


def get_bell_ringer(bell_ringer_id):
    """Get a specific bell ringer by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bell_ringers WHERE id = ?', (bell_ringer_id,))
        return cursor.fetchone()


def get_user_binder(handle):
    """Get all bell ringers in a user's binder"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT br.* FROM bell_ringers br
            INNER JOIN binder_items bi ON br.id = bi.bell_ringer_id
            WHERE bi.user_handle = ?
            ORDER BY bi.added_at DESC
        ''', (handle,))
        return cursor.fetchall()


def get_public_feed(sort_by='new'):
    """Get all public, approved bell ringers for the feed"""
    with get_db() as conn:
        cursor = conn.cursor()
        order_clause = 'created_at DESC' if sort_by == 'new' else 'binder_count DESC, created_at DESC'
        cursor.execute(f'''
            SELECT * FROM bell_ringers
            WHERE is_public = 1 AND is_approved = 1
            ORDER BY {order_clause}
        ''')
        return cursor.fetchall()


def add_to_binder(user_handle, bell_ringer_id):
    """Add a public bell ringer to user's binder"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Check if already in binder
        cursor.execute('''
            SELECT id FROM binder_items
            WHERE user_handle = ? AND bell_ringer_id = ?
        ''', (user_handle, bell_ringer_id))

        if cursor.fetchone():
            return False

        # Add to binder
        cursor.execute('''
            INSERT INTO binder_items (user_handle, bell_ringer_id, original_id)
            VALUES (?, ?, ?)
        ''', (user_handle, bell_ringer_id, bell_ringer_id))

        # Increment binder count
        cursor.execute('''
            UPDATE bell_ringers SET binder_count = binder_count + 1
            WHERE id = ?
        ''', (bell_ringer_id,))

        log_activity(user_handle, 'add_to_binder', f'Added bell ringer {bell_ringer_id} to binder', cursor=cursor)
        return True


def log_activity(user_handle, action_type, details='', cursor=None):
    """Log user activity for statistics

    Args:
        user_handle: User's handle
        action_type: Type of action performed
        details: Additional details about the action
        cursor: Optional database cursor to use (for nested transactions)
    """
    if cursor:
        # Use the provided cursor (nested transaction)
        cursor.execute('''
            INSERT INTO activity_logs (user_handle, action_type, details)
            VALUES (?, ?, ?)
        ''', (user_handle, action_type, details))
    else:
        # Create new connection (standalone call)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO activity_logs (user_handle, action_type, details)
                VALUES (?, ?, ?)
            ''', (user_handle, action_type, details))


def get_pending_approvals():
    """Get all bell ringers pending admin approval"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM bell_ringers
            WHERE is_public = 1 AND is_approved = 0
            ORDER BY created_at DESC
        ''')
        return cursor.fetchall()


def approve_bell_ringer(bell_ringer_id):
    """Approve a bell ringer for public display"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE bell_ringers SET is_approved = 1
            WHERE id = ?
        ''', (bell_ringer_id,))


def delete_bell_ringer(bell_ringer_id):
    """Delete a bell ringer (admin only)"""
    with get_db() as conn:
        cursor = conn.cursor()
        # Delete from binder items first
        cursor.execute('DELETE FROM binder_items WHERE bell_ringer_id = ?', (bell_ringer_id,))
        # Delete the bell ringer
        cursor.execute('DELETE FROM bell_ringers WHERE id = ?', (bell_ringer_id,))


def get_user_statistics():
    """Get statistics for all users (admin dashboard)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                u.handle,
                u.created_at,
                u.last_active,
                COUNT(DISTINCT CASE WHEN al.action_type = 'generate' THEN al.id END) as api_requests,
                COUNT(DISTINCT CASE WHEN al.action_type IN ('save', 'publish') THEN al.id END) as saves,
                COUNT(DISTINCT CASE WHEN al.action_type = 'login' THEN al.id END) as logins,
                COUNT(DISTINCT bi.id) as binder_items
            FROM users u
            LEFT JOIN activity_logs al ON u.handle = al.user_handle
            LEFT JOIN binder_items bi ON u.handle = bi.user_handle
            GROUP BY u.handle
            ORDER BY api_requests DESC
        ''')
        return cursor.fetchall()


def get_activity_summary():
    """Get overall activity summary for admin dashboard"""
    with get_db() as conn:
        cursor = conn.cursor()

        # Total counts
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM bell_ringers')
        total_bell_ringers = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM bell_ringers WHERE is_public = 1 AND is_approved = 1')
        public_bell_ringers = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM bell_ringers WHERE is_public = 1 AND is_approved = 0')
        pending_approvals = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM activity_logs WHERE action_type = "generate"')
        total_api_requests = cursor.fetchone()[0]

        return {
            'total_users': total_users,
            'total_bell_ringers': total_bell_ringers,
            'public_bell_ringers': public_bell_ringers,
            'pending_approvals': pending_approvals,
            'total_api_requests': total_api_requests
        }


def verify_admin(username, password_hash):
    """Verify admin credentials"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM admins WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        return cursor.fetchone() is not None


def create_admin(username, password_hash):
    """Create a new admin user"""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO admins (username, password_hash)
                VALUES (?, ?)
            ''', (username, password_hash))
            return True
        except sqlite3.IntegrityError:
            return False
