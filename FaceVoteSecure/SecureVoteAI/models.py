
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import json

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Voter(db.Model):
    __tablename__ = 'voters'
    
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    has_voted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    faces = db.relationship('VoterFace', backref='voter', lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='voter', lazy=True)
    auth_events = db.relationship('AuthEvent', backref='voter', lazy=True)
    
    def __repr__(self):
        return f'<Voter {self.voter_id}: {self.name}>'

class VoterFace(db.Model):
    __tablename__ = 'voter_faces'
    
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'), nullable=False)
    encoding = db.Column(db.Text, nullable=False)  # JSON serialized face encoding
    image_snapshot_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_encoding(self, encoding_array):
        """Store face encoding as JSON"""
        self.encoding = json.dumps(encoding_array.tolist() if hasattr(encoding_array, 'tolist') else encoding_array)
    
    def get_encoding(self):
        """Retrieve face encoding as numpy array"""
        import numpy as np
        return np.array(json.loads(self.encoding))
    
    def __repr__(self):
        return f'<VoterFace {self.id} for Voter {self.voter_id}>'

class Party(db.Model):
    __tablename__ = 'parties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    symbol_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    candidates = db.relationship('Candidate', backref='party', lazy=True, cascade='all, delete-orphan')
    
    def get_vote_count(self):
        """Get total votes for this party"""
        return sum(candidate.get_vote_count() for candidate in self.candidates)
    
    def __repr__(self):
        return f'<Party {self.name}>'

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    votes = db.relationship('Vote', backref='candidate', lazy=True)
    
    def get_vote_count(self):
        """Get vote count for this candidate"""
        return Vote.query.filter_by(candidate_id=self.id).count()
    
    def __repr__(self):
        return f'<Candidate {self.name} ({self.party.name})>'

class Vote(db.Model):
    __tablename__ = 'votes'
    
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'), nullable=False, unique=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=True)
    nota = db.Column(db.Boolean, default=False, nullable=False)
    cast_at = db.Column(db.DateTime, default=datetime.utcnow)
    audit_ref = db.Column(db.String(50), unique=True, nullable=False)
    
    __table_args__ = (
        db.CheckConstraint(
            '(candidate_id IS NOT NULL AND nota = false) OR (candidate_id IS NULL AND nota = true)',
            name='check_vote_choice'
        ),
    )
    
    @staticmethod
    def get_nota_count():
        """Get total NOTA votes"""
        return Vote.query.filter_by(nota=True).count()
    
    @staticmethod
    def get_total_votes():
        """Get total votes cast"""
        return Vote.query.count()
    
    def __repr__(self):
        choice = "NOTA" if self.nota else f"Candidate {self.candidate_id}"
        return f'<Vote {self.audit_ref}: {choice}>'

class AuthEvent(db.Model):
    __tablename__ = 'auth_events'
    
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'), nullable=True)
    voter_id_input = db.Column(db.String(50), nullable=False)
    result = db.Column(db.Enum('success', 'mismatch', 'unknown', name='auth_result'), nullable=False)
    distance = db.Column(db.Float, nullable=True)
    snapshot_path = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AuthEvent {self.id}: {self.result} for {self.voter_id_input}>'
