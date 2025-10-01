from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_limiter import Limiter
from werkzeug.security import check_password_hash
from . import auth_bp
import bcrypt
import os

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle admin and polling system login"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        login_type = data.get('type')  # 'Election Commission' or 'Polling System'

        # ✅ Hardcoded default admin credentials
        admin_user = "admin"
        admin_password = "admin123"

        if username == admin_user and password == admin_password:
            session['user_id'] = 'admin'
            session['user_type'] = login_type
            session['username'] = username

            if login_type == 'Election Commission':
                return redirect(url_for('admin.dashboard'))
            else:  # Polling System
                return redirect(url_for('poll.auth_start'))
        else:
            flash('Invalid credentials', 'error')

        if request.is_json:
            return jsonify({'success': False, 'message': 'Invalid credentials'})

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

def login_required(f):
    """Decorator to require login"""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin login"""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or session.get('user_type') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function