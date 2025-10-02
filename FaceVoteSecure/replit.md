# Smart Voting System

## Overview

A web-based electronic voting application with face recognition authentication. The system enables secure digital democracy through biometric verification, providing two main interfaces: an Election Commission admin panel for managing voters, parties, and candidates, and a Polling System for voter authentication and ballot casting. The application uses OpenCV-based face recognition to authenticate voters and automatically sends email notifications for successful votes and authentication failures.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (October 1, 2025)

### Authentication Fixes
- **Removed password hashing**: Simplified authentication to use hardcoded credentials (admin/admin123) without bcrypt hashing
- **Fixed routing bug**: Corrected session type mismatch that prevented Election Commission Dashboard buttons from working
  - Login form sends `type="admin"` for Election Commission selection
  - Login route now correctly checks for `login_type == 'admin'`
  - `admin_required` decorator accepts both 'admin' and 'Election Commission' types for backward compatibility
- **Added session['logged_in']**: Fixed missing session flag that caused authentication failures
- **Fixed JSON/redirect response mismatch**: Home page modal sends JSON requests, login now returns JSON with redirect URL instead of HTML redirect when request.is_json is true

### Management Pages Fixed
- **Manage Voters Page**: Added functional navigation buttons, voter listing table with pagination, and edit/delete/enroll face actions
- **Manage Parties Page**: Added functional navigation buttons, party card display with symbols, and edit/delete actions
- **Manage Candidates Page**: Added functional navigation buttons, candidate listing table with photos and party info, and edit/delete actions
- **Created Add/Edit Forms**: Complete forms for adding and editing voters, parties, and candidates with image upload and preview

### Results & Export Features
- **View Results Page**: Replaced placeholder JSON with full election results display including statistics, ranked candidate results, vote percentages, and winner highlight
- **CSV Export**: Download election results as comma-separated values with vote counts and percentages
- **Excel Export**: Generate XLSX spreadsheet with formatted election results (openpyxl installed)
- **PDF Export**: Create professional PDF reports with formatted tables using ReportLab
- **Fixed SQL Queries**: Corrected all results queries to use select_from(Vote) for proper data aggregation

### Email Configuration
- **Fixed Gmail app password**: Removed spaces from app password string (trqcsubsfkimwbrp) for proper SMTP authentication

### System Setup
- **Installed OpenGL dependencies**: Added libGL, libglvnd, and mesa system packages for OpenCV support
- **Initialized Replit PostgreSQL database**: Created and configured database with 6 tables (voters, voter_faces, parties, candidates, votes, auth_events)
- **Configured workflow**: Set up Flask server to run on port 5000 with webview output

### Verified Features
- 5-image face capture during voter registration (already implemented)
- Face recognition with success/failure flows (already implemented)
- Email notifications for authentication and voting (already implemented)
- Red blinking alert and beep sound on face mismatch (already implemented)

## System Architecture

### Backend Framework
- **Flask 3.1.2**: Main web framework with Blueprint-based modular architecture
- **Blueprints Structure**: Four separate blueprints for clean separation of concerns
  - `admin`: Election Commission management features (voters, parties, candidates)
  - `auth`: Login/logout and session management
  - `poll`: Voter authentication and voting flow
  - `results`: Vote tallying and reporting
- **Session-Based Authentication**: Uses Flask sessions for admin access control and voter state management
- **Rate Limiting**: Flask-Limiter configured for DDoS protection (1000/day, 100/hour per IP)

### Database Architecture
- **SQLAlchemy ORM**: Database abstraction layer with declarative base models
- **Flask-Migrate**: Alembic-based database migrations
- **Core Models**:
  - `Voter`: Stores voter demographics (ID, name, age, DOB, gender, email, voting status)
  - `VoterFace`: Stores JSON-serialized face encodings (up to 5 per voter) with snapshot paths
  - `Party`: Political party information with symbol image paths
  - `Candidate`: Candidate details linked to parties
  - `Vote`: Encrypted vote records with audit references
  - `AuthEvent`: Authentication attempt logs with IP/user agent tracking
- **Relationships**: One-to-many cascading deletes between voters and face encodings
- **Database URL**: Configurable via environment variable, defaults to local PostgreSQL

### Face Recognition System
- **OpenCV-based Detection**: Uses Haar Cascade classifiers for face and eye detection
- **Feature Extraction**: Multi-feature approach combining:
  - Histogram features (256-bin grayscale distribution)
  - LBP-like texture descriptors
  - Normalized 64x64 face templates
- **Matching Algorithm**: Euclidean distance comparison with configurable threshold (default 0.6)
- **Enrollment Process**: Captures 1-5 images per voter for improved accuracy
- **Verification Flow**: Compares captured image against all stored encodings for a voter
- **Liveness Detection**: Eye cascade detection to prevent photo-based spoofing

### Email Notification System
- **Gmail SMTP**: Flask-Mail with TLS encryption (port 587)
- **App Password Authentication**: Uses dedicated app password (not personal password)
- **Threaded Sending**: Async email dispatch to avoid blocking requests
- **Three Email Types**:
  1. **Authentication Success**: Sent to voter after successful face match
  2. **Fake Face Alert**: Sent to commissioner and voter with captured photo attachment when face doesn't match
  3. **Vote Confirmation**: Sent to voter with choice, audit reference, and timestamp
- **Email Content**: Includes voter ID, timestamps (UTC and local), distance scores, IP addresses

### Authentication & Authorization
- **Admin Login**: Default credentials (admin/admin123) without password hashing (simplified as requested)
- **Dual Access Paths**: 
  - Election Commission → Admin dashboard (login form type="admin")
  - Polling System → Voter authentication (login form type="polling")
- **Session Gating**: 
  - Admin routes protected by `@admin_required` decorator (checks for 'admin' or 'Election Commission' session type)
  - Voter ballot access controlled via `session['authenticated_voter_id']`
- **Voter Flow**: Face authentication → Session token → Ballot access (no admin login required)
- **Security**: Session-based authentication with `logged_in` flag, CSRF protection via Flask-WTF

### Frontend Architecture
- **Template Engine**: Jinja2 with base template inheritance
- **Styling**: Bootstrap 5.1.3 with custom CSS overlays
- **Webcam Integration**: getUserMedia API for real-time video capture
- **Visual Feedback**:
  - Green success alerts on successful authentication
  - Red blinking screen animation on fake face detection
  - Audio beep alerts using base64-encoded WAV data
- **Image Handling**: Canvas API for base64 encoding, client-side preview generation

### Vote Casting & Auditing
- **Ballot Generation**: Dynamic rendering from Party-Candidate relationships
- **NOTA Support**: "None of the Above" option included by default
- **Vote Recording**: UUID-based audit references for traceability
- **Double-Vote Prevention**: Database-level `has_voted` flag check
- **Success Flow**: Vote submission → Email notification → Auto-redirect to success page

### File Storage
- **Party Symbols**: Uploaded to `static/uploads/party_symbols/` with secure filename sanitization
- **Candidate Photos**: Stored in `static/uploads/candidate_photos/`
- **Face Snapshots**: Saved to `static/uploads/face_snapshots/` for audit trail
- **Image Validation**: File type and size checks before storage

### Error Handling & Logging
- **Flash Messages**: Bootstrap alert integration for user feedback
- **Authentication Logging**: All attempts recorded in `AuthEvent` table with IP/user agent
- **Database Error Handling**: Pool pre-ping and connection recycling (300s timeout)
- **Graceful Degradation**: Fallback UI when webcam access fails

## External Dependencies

### Database
- **PostgreSQL 16**: Primary relational database
- **psycopg2-binary 2.9.10**: PostgreSQL adapter for Python
- **Connection Pooling**: SQLAlchemy engine with pre-ping health checks

### AI/ML Libraries
- **OpenCV (cv2) 4.11.0.86**: Computer vision for face detection and feature extraction
- **NumPy 2.3.3**: Numerical operations for face encoding arrays
- **Pillow 11.3.0**: Image processing and format conversion

### Email Service
- **Gmail SMTP**: smtp.gmail.com:587 with TLS
- **Sender**: electioncomission101@gmail.com (with app password: trqcsubsfkimwbrp)
- **Alert Recipient**: mithraa1906@gmail.com (Election Commissioner)
- **Flask-Mail 0.10.0**: Email integration library

### Security & Utilities
- **python-dotenv 1.1.1**: Environment variable management
- **Flask-WTF 1.2.2**: CSRF protection and form handling
- **Flask-Limiter 4.0.0**: Rate limiting middleware

### Reporting & Export
- **Pandas 2.3.2**: Data manipulation for result exports
- **ReportLab 4.4.4**: PDF generation for election reports

### Development Tools
- **Flask-Migrate 4.1.0**: Database migration management (Alembic wrapper)
- **pytest 8.4.2**: Testing framework
- **Werkzeug**: WSGI utilities and secure filename generation

### Environment Configuration
- **Required Variables**:
  - `DATABASE_URL`: PostgreSQL connection string
  - `SECRET_KEY`: Flask session encryption key
  - `EMAIL_USER`: Gmail sender address
  - `EMAIL_APP_PASSWORD`: Gmail app password
  - `ADMIN_DEFAULT_USER`: Admin username (default: admin)
  - `ADMIN_DEFAULT_PASSWORD`: Admin password (default: admin123)
  - `FACE_THRESHOLD`: Face matching threshold (default: 0.6)
  - `ALERT_RECIPIENT`: Commissioner email for alerts