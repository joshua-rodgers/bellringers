"""
Main routes for Bell Ringers blueprint
"""
from flask import Blueprint, render_template, request, jsonify, session
import random
from . import database as db
from . import gemini_api

bp = Blueprint('bellringers', __name__, template_folder='templates', static_folder='static')


@bp.route('/')
def index():
    """Main generator page with Lock & Spin UI"""
    return render_template('generator.html',
                         topics=gemini_api.get_topic_options(),
                         formats=gemini_api.get_format_options(),
                         constraints=gemini_api.get_constraint_options())


@bp.route('/api/generate', methods=['POST'])
def generate():
    """
    Generate a bell ringer based on locked/unlocked slots
    Expects JSON: {topic, format, constraint, locked_slots: []}
    """
    data = request.get_json()
    user_handle = session.get('user_handle')

    if not user_handle:
        return jsonify({'error': 'No user session'}), 401

    topic = data.get('topic')
    format_type = data.get('format')
    constraint = data.get('constraint')

    # Generate using Gemini API
    try:
        content = gemini_api.generate_bell_ringer(topic, format_type, constraint)

        # Log the API request
        db.log_activity(user_handle, 'generate', f'{topic} - {format_type} - {constraint}')
        db.update_last_active(user_handle)

        return jsonify({
            'success': True,
            'content': content,
            'topic': topic,
            'format': format_type,
            'constraint': constraint
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/spin', methods=['POST'])
def spin_slots():
    """
    Spin unlocked slots and return random values
    Expects JSON: {locked: {topic: bool, format: bool, constraint: bool}}
    """
    data = request.get_json()
    locked = data.get('locked', {})

    result = {}

    if not locked.get('topic'):
        result['topic'] = random.choice(gemini_api.get_topic_options())

    if not locked.get('format'):
        result['format'] = random.choice(gemini_api.get_format_options())

    if not locked.get('constraint'):
        result['constraint'] = random.choice(gemini_api.get_constraint_options())

    return jsonify(result)


@bp.route('/api/save', methods=['POST'])
def save():
    """Save a bell ringer to user's private binder"""
    data = request.get_json()
    user_handle = session.get('user_handle')

    if not user_handle:
        return jsonify({'error': 'No user session'}), 401

    try:
        bell_ringer_id = db.save_bell_ringer(
            owner_handle=user_handle,
            topic=data.get('topic'),
            format_type=data.get('format'),
            constraint=data.get('constraint'),
            content=data.get('content'),
            is_public=False
        )

        return jsonify({'success': True, 'id': bell_ringer_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/publish', methods=['POST'])
def publish():
    """Publish a bell ringer to the public feed (requires admin approval)"""
    data = request.get_json()
    user_handle = session.get('user_handle')

    if not user_handle:
        return jsonify({'error': 'No user session'}), 401

    try:
        bell_ringer_id = db.save_bell_ringer(
            owner_handle=user_handle,
            topic=data.get('topic'),
            format_type=data.get('format'),
            constraint=data.get('constraint'),
            content=data.get('content'),
            is_public=True
        )

        return jsonify({
            'success': True,
            'id': bell_ringer_id,
            'message': 'Published! Awaiting admin approval.'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/add-to-binder/<int:bell_ringer_id>', methods=['POST'])
def add_to_binder(bell_ringer_id):
    """Add a public bell ringer to user's binder"""
    user_handle = session.get('user_handle')

    if not user_handle:
        return jsonify({'error': 'No user session'}), 401

    try:
        success = db.add_to_binder(user_handle, bell_ringer_id)
        if success:
            return jsonify({'success': True, 'message': 'Added to your binder!'})
        else:
            return jsonify({'success': False, 'message': 'Already in your binder'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/binder')
def binder():
    """My Binder page - user's private collection"""
    user_handle = session.get('user_handle')

    if not user_handle:
        return render_template('binder.html', bell_ringers=[], error='No user session')

    bell_ringers = db.get_user_binder(user_handle)
    return render_template('binder.html', bell_ringers=bell_ringers)


@bp.route('/feed')
def feed():
    """The Feed page - public bell ringers"""
    sort_by = request.args.get('sort', 'new')
    bell_ringers = db.get_public_feed(sort_by)
    user_handle = session.get('user_handle')

    return render_template('feed.html',
                         bell_ringers=bell_ringers,
                         sort_by=sort_by,
                         user_handle=user_handle)


@bp.route('/print/<int:bell_ringer_id>')
def print_view(bell_ringer_id):
    """Print-optimized view for a bell ringer"""
    bell_ringer = db.get_bell_ringer(bell_ringer_id)

    if not bell_ringer:
        return "Bell ringer not found", 404

    return render_template('print.html', bell_ringer=bell_ringer)


@bp.before_request
def ensure_user():
    """Ensure user has a handle before each request"""
    if 'user_handle' not in session and request.endpoint not in ['bellringers.static', 'admin.login']:
        # This will be set by JavaScript on first visit
        pass
