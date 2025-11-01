"""
Main routes for Bell Ringers blueprint
"""
from flask import render_template, request, jsonify, session
import random
from . import database as db
from . import gemini_api
from . import standards as standards_module


def register_routes(bp):
    """Register all main routes to the blueprint"""

    @bp.route('/')
    def index():
        """Main generator page with Lock & Spin UI"""
        return render_template('bellringers/generator.html',
                             topics=gemini_api.get_topic_options(),
                             formats=gemini_api.get_format_options(),
                             constraints=gemini_api.get_constraint_options(),
                             standards=standards_module.get_standards_list())

    @bp.route('/api/generate', methods=['POST'])
    def generate():
        """
        Generate a bell ringer based on parameters
        Expects JSON: {topic, format, constraint, prompt, standards: []}
        """
        data = request.get_json()
        user_handle = session.get('user_handle')

        if not user_handle:
            return jsonify({'error': 'No user session'}), 401

        topic = data.get('topic')
        format_type = data.get('format')
        constraint = data.get('constraint')
        prompt = data.get('prompt', '')
        standard_codes = data.get('standards', [])

        # Generate using Gemini API
        try:
            content = gemini_api.generate_bell_ringer(topic, format_type, constraint, standard_codes, prompt)

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

        print(f"Binder page - Session data: {dict(session)}")  # Debug logging

        if not user_handle:
            error_msg = 'No user session. Please reload the page to create a session.'
            return render_template('bellringers/binder.html', bell_ringers=[], error=error_msg)

        bell_ringers = db.get_user_binder(user_handle)
        return render_template('bellringers/binder.html', bell_ringers=bell_ringers)

    @bp.route('/api/debug/session')
    def debug_session():
        """Debug endpoint to check session state"""
        return jsonify({
            'session_data': dict(session),
            'user_handle': session.get('user_handle'),
            'has_session': bool(session)
        })

    @bp.route('/debug')
    def debug_page():
        """Debug page for testing session flow"""
        return render_template('bellringers/debug_session.html')

    @bp.route('/feed')
    def feed():
        """The Feed page - public bell ringers"""
        sort_by = request.args.get('sort', 'new')
        bell_ringers = db.get_public_feed(sort_by)
        user_handle = session.get('user_handle')

        return render_template('bellringers/feed.html',
                             bell_ringers=bell_ringers,
                             sort_by=sort_by,
                             user_handle=user_handle)

    @bp.route('/print/<int:bell_ringer_id>')
    def print_view(bell_ringer_id):
        """Print-optimized view for a bell ringer"""
        bell_ringer = db.get_bell_ringer(bell_ringer_id)

        if not bell_ringer:
            return "Bell ringer not found", 404

        return render_template('bellringers/print.html', bell_ringer=bell_ringer)
