from flask import render_template, request, redirect, url_for, flash, jsonify, session, current_app
from flask_mail import Mail
from . import poll_bp
from models import db, Voter, VoterFace, Party, Candidate, Vote, AuthEvent
from services.face_service import FaceService
from services.email_service import EmailService
import os
import uuid
from datetime import datetime

@poll_bp.route('/auth/start')
def auth_start():
    """Start voter authentication"""
    return render_template('poll/auth.html')

@poll_bp.route('/auth/verify', methods=['POST'])
def verify_auth():
    """Verify voter authentication via face recognition with AI liveness detection"""
    try:
        data = request.json
        voter_id_input = data.get('voter_id')
        image_data = data.get('image_data')

        if not voter_id_input or not image_data:
            return jsonify({'success': False, 'message': 'Missing voter ID or image data'})

        # Find voter
        voter = Voter.query.filter_by(voter_id=voter_id_input).first()

        if not voter:
            # Log unknown voter attempt
            auth_event = AuthEvent(
                voter_id_input=voter_id_input,
                result='unknown',
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')
            )
            db.session.add(auth_event)
            db.session.commit()
            return jsonify({'success': False, 'message': 'Voter ID not found'})

        # Check if already voted
        if voter.has_voted:
            return jsonify({'success': False, 'message': 'You have already voted'})

        # Get stored face encodings
        face_encodings = [face.get_encoding() for face in voter.faces]

        if not face_encodings:
            return jsonify({'success': False, 'message': 'No face data enrolled for this voter'})

        # Initialize face service with configured threshold (0.30 for VGG-Face cosine distance)
        threshold = current_app.config.get('FACE_THRESHOLD', 0.30)
        face_service = FaceService(threshold=threshold)
        current_app.logger.info(f"Initialized FaceService with threshold: {threshold}")

        # AI Liveness Detection (anti-spoofing)
        liveness_result = face_service.ai_liveness_detection(image_data)
        current_app.logger.info(f"Liveness detection result for voter {voter_id_input}: {liveness_result}")

        # Only reject if AI explicitly detected a fake face (is_live = False)
        # If is_live = None (AI not available), skip liveness check and rely on face matching
        if liveness_result.get('is_live') == False:
            current_app.logger.warning(f"AI detected fake face for voter {voter_id_input}")
            # Fake face detected by AI
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            snapshot_filename = f"fake_{voter.voter_id}_{timestamp}.jpg"
            snapshot_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                        'fraud_attempts', 
                                        snapshot_filename)
            face_service.save_image_from_base64(image_data, snapshot_path)

            # Log fake face attempt
            auth_event = AuthEvent(
                voter_id=voter.id,
                voter_id_input=voter_id_input,
                result='mismatch',
                distance=1.0,
                snapshot_path=snapshot_path,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')
            )
            db.session.add(auth_event)
            db.session.commit()

            # Send alert email
            email_service = EmailService(mail_instance=current_app.extensions.get('mail'))
            email_service.send_auth_failure_alert(
                voter_id_input=voter_id_input,
                voter_email=voter.email,
                distance=1.0,
                snapshot_path=snapshot_path,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')
            )

            return jsonify({
                'success': False,
                'message': f'Fake face detected! {liveness_result.get("reason", "")}',
                'fake_face': True,
                'ai_detected': True,
                'distance': 1.0
            })

        # Log if AI liveness detection was skipped or failed
        if liveness_result.get('is_live') is None:
            ai_reason = liveness_result.get('reason', 'Unknown')
            current_app.logger.warning(f"AI liveness detection unavailable for voter {voter_id_input}: {ai_reason}")
            current_app.logger.warning(f"Relying on face matching only (threshold: {current_app.config['FACE_THRESHOLD']}) - Consider configuring OPENAI_API_KEY or GEMINI_API_KEY for enhanced security")

        # Encode captured face
        test_encoding = face_service.encode_face_from_base64(image_data)

        if test_encoding is None:
            return jsonify({'success': False, 'message': 'No face detected in image. Please try again'})

        # Verify face against stored encodings
        is_match, distance = face_service.verify_face(face_encodings, test_encoding)

        # Save snapshot
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        snapshot_filename = f"auth_{voter.voter_id}_{timestamp}.jpg"
        snapshot_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                    'fraud_attempts' if not is_match else 'faces', 
                                    snapshot_filename)
        face_service.save_image_from_base64(image_data, snapshot_path)

        # Log auth event
        auth_event = AuthEvent(
            voter_id=voter.id,
            voter_id_input=voter_id_input,
            result='success' if is_match else 'mismatch',
            distance=distance,
            snapshot_path=snapshot_path,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        db.session.add(auth_event)
        db.session.commit()

        if is_match:
            # Success - store in session
            session['authenticated_voter_id'] = voter.id
            session['voter_name'] = voter.name

            # Send success email
            email_service = EmailService(mail_instance=current_app.extensions.get('mail'))
            email_service.send_auth_success(
                voter_email=voter.email,
                voter_name=voter.name
            )

            return jsonify({
                'success': True,
                'message': 'Authentication successful! Face verified.',
                'redirect': url_for('poll.ballot')
            })
        else:
            # Failure - send alert emails (this is a face mismatch, not necessarily fake)
            email_service = EmailService(mail_instance=current_app.extensions.get('mail'))
            email_service.send_auth_failure_alert(
                voter_id_input=voter_id_input,
                voter_email=voter.email,
                distance=distance,
                snapshot_path=snapshot_path,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')
            )

            return jsonify({
                'success': False,
                'message': f'Face does not match voter ID. Distance: {distance:.2f}',
                'fake_face': True,  # Not flagging as fake - just a mismatch
                'distance': distance
            })

    except Exception as e:
        current_app.logger.error(f"Error in verify_auth: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Authentication error: {str(e)}'})

@poll_bp.route('/ballot')
def ballot():
    """Show voting ballot"""
    # Check if authenticated
    if 'authenticated_voter_id' not in session:
        flash('Please authenticate first', 'error')
        return redirect(url_for('poll.auth_start'))

    # Get all parties with candidates
    parties = Party.query.all()

    return render_template('poll/ballot.html', parties=parties)

@poll_bp.route('/vote', methods=['POST'])
def cast_vote():
    """Cast a vote"""
    try:
        # Check if authenticated
        if 'authenticated_voter_id' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'})

        voter_id = session['authenticated_voter_id']
        voter = Voter.query.get(voter_id)

        if not voter:
            return jsonify({'success': False, 'message': 'Voter not found'})

        if voter.has_voted:
            return jsonify({'success': False, 'message': 'Already voted'})

        data = request.json
        candidate_id = data.get('candidate_id')
        nota = data.get('nota', False)

        # Validate vote choice
        if not nota and not candidate_id:
            return jsonify({'success': False, 'message': 'Please select a candidate or NOTA'})

        if nota and candidate_id:
            return jsonify({'success': False, 'message': 'Cannot select both candidate and NOTA'})

        # Generate audit reference
        audit_ref = str(uuid.uuid4())[:8].upper()

        # Create vote
        vote = Vote(
            voter_id=voter.id,
            candidate_id=int(candidate_id) if candidate_id and not nota else None,
            nota=nota,
            audit_ref=audit_ref
        )

        # Mark voter as voted
        voter.has_voted = True

        db.session.add(vote)
        db.session.commit()

        # Determine choice for email
        if nota:
            choice = "NOTA (None of the Above)"
        else:
            candidate = Candidate.query.get(int(candidate_id))
            choice = f"{candidate.name} ({candidate.party.name})" if candidate else "Unknown"

        # Send confirmation email
        email_service = EmailService(mail_instance=current_app.extensions.get('mail'))
        email_service.send_vote_confirmation(
            voter_email=voter.email,
            voter_name=voter.name,
            choice=choice,
            audit_ref=audit_ref
        )

        # Clear session
        session.pop('authenticated_voter_id', None)
        session.pop('voter_name', None)

        return jsonify({
            'success': True,
            'message': 'Vote cast successfully',
            'audit_ref': audit_ref,
            'redirect': url_for('poll.success')
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error casting vote: {str(e)}")
        return jsonify({'success': False, 'message': f'Error casting vote: {str(e)}'})

@poll_bp.route('/success')
def success():
    """Show vote success"""
    return render_template('poll/success.html')