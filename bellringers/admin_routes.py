"""
Admin routes for Bell Ringers blueprint
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import hashlib
from . import database as db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


def require_admin():
    """Decorator to require admin authentication"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    return None


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')

        if username and password:
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            if db.verify_admin(username, password_hash):
                session['admin_logged_in'] = True
                session['admin_username'] = username

                if request.is_json:
                    return jsonify({'success': True})
                else:
                    return redirect(url_for('admin.dashboard'))

        if request.is_json:
            return jsonify({'error': 'Invalid credentials'}), 401
        else:
            return render_template('admin/login.html', error='Invalid credentials')

    return render_template('admin/login.html')


@admin_bp.route('/logout')
def logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
def dashboard():
    """Admin dashboard with statistics"""
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    # Get overall statistics
    summary = db.get_activity_summary()
    user_stats = db.get_user_statistics()

    return render_template('admin/dashboard.html',
                         summary=summary,
                         user_stats=user_stats)


@admin_bp.route('/content')
def content():
    """Admin content management page"""
    redirect_response = require_admin()
    if redirect_response:
        return redirect_response

    # Get pending approvals
    pending = db.get_pending_approvals()

    # Get all public bell ringers
    all_public = db.get_public_feed('new')

    return render_template('admin/content.html',
                         pending=pending,
                         all_public=all_public)


@admin_bp.route('/api/approve/<int:bell_ringer_id>', methods=['POST'])
def approve(bell_ringer_id):
    """Approve a bell ringer for public display"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        db.approve_bell_ringer(bell_ringer_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/api/delete/<int:bell_ringer_id>', methods=['POST'])
def delete(bell_ringer_id):
    """Delete a bell ringer"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        db.delete_bell_ringer(bell_ringer_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
