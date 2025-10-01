from flask import render_template, request, redirect, url_for, flash, jsonify
from . import poll_bp
from blueprints.auth.routes import login_required

@poll_bp.route('/auth/start')
@login_required
def auth_start():
    """Start voter authentication"""
    return render_template('poll/auth.html')

@poll_bp.route('/ballot')
@login_required
def ballot():
    """Show voting ballot"""
    return render_template('poll/ballot.html')

@poll_bp.route('/success')
@login_required
def success():
    """Show vote success"""
    return render_template('poll/success.html')