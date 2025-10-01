from flask import render_template, request, redirect, url_for, flash, jsonify
from . import results_bp

@results_bp.route('/live')
def live():
    """Live results"""
    return jsonify({'message': 'Live results endpoint'})