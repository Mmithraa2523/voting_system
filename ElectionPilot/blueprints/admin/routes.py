from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime, date
from . import admin_bp
from blueprints.auth.routes import admin_required
from models import db, Voter, VoterFace, Party, Candidate, Vote, AuthEvent
from services.face_service import FaceService
import json

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    total_voters = Voter.query.count()
    total_parties = Party.query.count()
    total_candidates = Candidate.query.count()
    total_votes = Vote.query.count()
    
    stats = {
        'total_voters': total_voters,
        'total_parties': total_parties,
        'total_candidates': total_candidates,
        'total_votes': total_votes,
        'voter_turnout': (total_votes / total_voters * 100) if total_voters > 0 else 0
    }
    
    return render_template('admin/dashboard.html', stats=stats)

# VOTERS MANAGEMENT
@admin_bp.route('/voters')
@admin_required
def voters():
    """Manage voters"""
    page = request.args.get('page', 1, type=int)
    voters = Voter.query.paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/voters.html', voters=voters)

@admin_bp.route('/voters/add', methods=['GET', 'POST'])
@admin_required
def add_voter():
    """Add new voter"""
    if request.method == 'POST':
        try:
            # Get form data
            voter_id = request.form.get('voter_id')
            name = request.form.get('name')
            age = int(request.form.get('age'))
            dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d').date()
            gender = request.form.get('gender')
            email = request.form.get('email')
            
            # Check if voter ID already exists
            if Voter.query.filter_by(voter_id=voter_id).first():
                flash('Voter ID already exists', 'error')
                return render_template('admin/add_voter.html')
            
            # Check if email already exists
            if Voter.query.filter_by(email=email).first():
                flash('Email already exists', 'error')
                return render_template('admin/add_voter.html')
            
            # Create new voter
            voter = Voter(
                voter_id=voter_id,
                name=name,
                age=age,
                dob=dob,
                gender=gender,
                email=email
            )
            
            db.session.add(voter)
            db.session.commit()
            
            flash('Voter added successfully', 'success')
            return redirect(url_for('admin.voters'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding voter: {str(e)}', 'error')
    
    return render_template('admin/add_voter.html')

@admin_bp.route('/voters/<int:voter_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_voter(voter_id):
    """Edit voter"""
    voter = Voter.query.get_or_404(voter_id)
    
    if request.method == 'POST':
        try:
            voter.name = request.form.get('name')
            voter.age = int(request.form.get('age'))
            voter.dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d').date()
            voter.gender = request.form.get('gender')
            voter.email = request.form.get('email')
            voter.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Voter updated successfully', 'success')
            return redirect(url_for('admin.voters'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating voter: {str(e)}', 'error')
    
    return render_template('admin/edit_voter.html', voter=voter)

@admin_bp.route('/voters/<int:voter_id>/delete', methods=['POST'])
@admin_required
def delete_voter(voter_id):
    """Delete voter"""
    try:
        voter = Voter.query.get_or_404(voter_id)
        db.session.delete(voter)
        db.session.commit()
        flash('Voter deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting voter: {str(e)}', 'error')
    
    return redirect(url_for('admin.voters'))

@admin_bp.route('/voters/<int:voter_id>/enroll-face')
@admin_required
def enroll_face(voter_id):
    """Face enrollment page"""
    voter = Voter.query.get_or_404(voter_id)
    return render_template('admin/enroll_face.html', voter=voter)

@admin_bp.route('/voters/<int:voter_id>/enroll-face', methods=['POST'])
@admin_required
def process_face_enrollment(voter_id):
    """Process face enrollment"""
    try:
        voter = Voter.query.get_or_404(voter_id)
        face_service = FaceService(threshold=current_app.config['FACE_THRESHOLD'])
        
        # Get image data from request
        image_data = request.json.get('image_data')
        
        if not image_data:
            return jsonify({'success': False, 'message': 'No image data provided'})
        
        # Extract face encoding
        encoding = face_service.encode_face_from_base64(image_data)
        
        if encoding is None:
            return jsonify({'success': False, 'message': 'No face detected in image'})
        
        # Save face encoding
        face_record = VoterFace(voter_id=voter.id)
        face_record.set_encoding(encoding)
        
        # Optionally save snapshot
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"voter_{voter.voter_id}_{timestamp}.jpg"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'faces', filename)
        
        if face_service.save_image_from_base64(image_data, filepath):
            face_record.image_snapshot_path = filepath
        
        db.session.add(face_record)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Face enrolled successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error enrolling face: {str(e)}'})

# PARTIES MANAGEMENT
@admin_bp.route('/parties')
@admin_required
def parties():
    """Manage parties"""
    parties = Party.query.all()
    return render_template('admin/parties.html', parties=parties)

@admin_bp.route('/parties/add', methods=['GET', 'POST'])
@admin_required
def add_party():
    """Add new party"""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            
            # Check if party name already exists
            if Party.query.filter_by(name=name).first():
                flash('Party name already exists', 'error')
                return render_template('admin/add_party.html')
            
            party = Party(name=name)
            
            # Handle symbol upload
            if 'symbol' in request.files:
                file = request.files['symbol']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    # Add unique identifier to prevent conflicts
                    unique_filename = f"{uuid.uuid4()}_{filename}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'party_symbols', unique_filename)
                    file.save(filepath)
                    party.symbol_path = filepath
            
            db.session.add(party)
            db.session.commit()
            
            flash('Party added successfully', 'success')
            return redirect(url_for('admin.parties'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding party: {str(e)}', 'error')
    
    return render_template('admin/add_party.html')

@admin_bp.route('/parties/<int:party_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_party(party_id):
    """Edit party"""
    party = Party.query.get_or_404(party_id)
    
    if request.method == 'POST':
        try:
            party.name = request.form.get('name')
            
            # Handle symbol upload
            if 'symbol' in request.files:
                file = request.files['symbol']
                if file and file.filename:
                    # Delete old symbol if exists
                    if party.symbol_path and os.path.exists(party.symbol_path):
                        os.remove(party.symbol_path)
                    
                    filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4()}_{filename}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'party_symbols', unique_filename)
                    file.save(filepath)
                    party.symbol_path = filepath
            
            party.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('Party updated successfully', 'success')
            return redirect(url_for('admin.parties'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating party: {str(e)}', 'error')
    
    return render_template('admin/edit_party.html', party=party)

@admin_bp.route('/parties/<int:party_id>/delete', methods=['POST'])
@admin_required
def delete_party(party_id):
    """Delete party"""
    try:
        party = Party.query.get_or_404(party_id)
        
        # Delete symbol file if exists
        if party.symbol_path and os.path.exists(party.symbol_path):
            os.remove(party.symbol_path)
        
        db.session.delete(party)
        db.session.commit()
        flash('Party deleted successfully', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting party: {str(e)}', 'error')
    
    return redirect(url_for('admin.parties'))

# CANDIDATES MANAGEMENT
@admin_bp.route('/candidates')
@admin_required
def candidates():
    """Manage candidates"""
    candidates = Candidate.query.join(Party).all()
    parties = Party.query.all()
    return render_template('admin/candidates.html', candidates=candidates, parties=parties)

@admin_bp.route('/candidates/add', methods=['GET', 'POST'])
@admin_required
def add_candidate():
    """Add new candidate"""
    parties = Party.query.all()
    
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            party_id = int(request.form.get('party_id'))
            
            candidate = Candidate(name=name, party_id=party_id)
            
            # Handle image upload
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4()}_{filename}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'candidate_images', unique_filename)
                    file.save(filepath)
                    candidate.image_path = filepath
            
            db.session.add(candidate)
            db.session.commit()
            
            flash('Candidate added successfully', 'success')
            return redirect(url_for('admin.candidates'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding candidate: {str(e)}', 'error')
    
    return render_template('admin/add_candidate.html', parties=parties)

@admin_bp.route('/candidates/<int:candidate_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_candidate(candidate_id):
    """Edit candidate"""
    candidate = Candidate.query.get_or_404(candidate_id)
    parties = Party.query.all()
    
    if request.method == 'POST':
        try:
            candidate.name = request.form.get('name')
            candidate.party_id = int(request.form.get('party_id'))
            
            # Handle image upload
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    # Delete old image if exists
                    if candidate.image_path and os.path.exists(candidate.image_path):
                        os.remove(candidate.image_path)
                    
                    filename = secure_filename(file.filename)
                    unique_filename = f"{uuid.uuid4()}_{filename}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'candidate_images', unique_filename)
                    file.save(filepath)
                    candidate.image_path = filepath
            
            candidate.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('Candidate updated successfully', 'success')
            return redirect(url_for('admin.candidates'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating candidate: {str(e)}', 'error')
    
    return render_template('admin/edit_candidate.html', candidate=candidate, parties=parties)

@admin_bp.route('/candidates/<int:candidate_id>/delete', methods=['POST'])
@admin_required
def delete_candidate(candidate_id):
    """Delete candidate"""
    try:
        candidate = Candidate.query.get_or_404(candidate_id)
        
        # Delete image file if exists
        if candidate.image_path and os.path.exists(candidate.image_path):
            os.remove(candidate.image_path)
        
        db.session.delete(candidate)
        db.session.commit()
        flash('Candidate deleted successfully', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting candidate: {str(e)}', 'error')
    
    return redirect(url_for('admin.candidates'))

# ROLLBACK FUNCTIONALITY
@admin_bp.route('/rollback-votes', methods=['POST'])
@admin_required
def rollback_votes():
    """Rollback all votes and reset election - clears all voting history"""
    try:
        # Delete all votes
        Vote.query.delete()
        
        # Delete all auth events
        AuthEvent.query.delete()
        
        # Reset all voters' has_voted status
        voters = Voter.query.all()
        for voter in voters:
            voter.has_voted = False
        
        db.session.commit()
        
        flash('All voting history has been cleared successfully. Election can be restarted fresh.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error during rollback: {str(e)}', 'error')
    
    return redirect(url_for('admin.dashboard'))