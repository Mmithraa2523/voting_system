
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file, send_from_directory
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import cv2
import numpy as np
import base64
from PIL import Image
import io
import json
import uuid
from datetime import datetime
import threading

# Load environment variables
load_dotenv()

# Import db from models
from models import db
from utils import normalize_path_for_url, get_url_path

# Initialize extensions
migrate = Migrate()
mail = Mail()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"]
)

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', os.environ.get('SECRET_KEY', 'bdb6766f351e0a56669f4385007a2362a72e50f1068dd4d4efcc5d1f6009217f'))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:12345@localhost:5432/smart_voting')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_APP_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_FROM', f'Election Commission <{app.config["MAIL_USERNAME"]}>')
    
    # Validate required email configuration
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print("WARNING: Email credentials not configured. Email notifications will be disabled.")
        print("Please set EMAIL_USER and EMAIL_APP_PASSWORD environment variables.")
    
    # App specific configuration
    app.config['FACE_THRESHOLD'] = float(os.environ.get('FACE_THRESHOLD', '0.35'))
    app.config['ALERT_RECIPIENT'] = os.environ.get('ALERT_RECIPIENT', 'mithraa1906@gmail.com')
    app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_DEFAULT_USER', 'admin')
    app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_DEFAULT_PASSWORD', 'admin123')
    
    # File upload configuration - store in static/uploads for easy access
    app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    # Create upload directories
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'faces'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'fraud_attempts'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'party_symbols'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'candidate_images'), exist_ok=True)
    
    # Import models to ensure they're created
    from models import Voter, VoterFace, Party, Candidate, Vote, AuthEvent
    
    # Register blueprints
    from blueprints.auth import auth_bp
    from blueprints.admin import admin_bp
    from blueprints.poll import poll_bp
    from blueprints.results import results_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(poll_bp, url_prefix='/poll')
    app.register_blueprint(results_bp, url_prefix='/results')
    
    # Main landing page
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Route to serve uploaded files
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        """Serve uploaded files from static/uploads directory"""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # Add custom Jinja filters
    app.jinja_env.filters['url_path'] = get_url_path
    app.jinja_env.filters['normalize_path'] = normalize_path_for_url
    
    # Create database tables (run init_db.py separately to initialize)
    # with app.app_context():
    #     db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Set debug based on environment
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Always bind to 0.0.0.0:5000 for Replit
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
