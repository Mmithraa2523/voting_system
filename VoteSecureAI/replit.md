# Smart Voting System

## Overview

A web-based electronic voting application with face recognition authentication. The system provides two main interfaces: an Election Commission admin panel for managing voters, parties, and candidates, and a Polling System for voters to authenticate and cast votes securely. Face recognition ensures voter identity verification, while automated email alerts notify stakeholders of successful votes and security incidents.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

### October 2, 2025 - Production Deployment Setup
- **Database Setup**: Configured PostgreSQL database using Replit's built-in database service
- **Workflow Configuration**: Set up Flask Server workflow running on 0.0.0.0:5000 for Replit deployment
- **Upload Directories**: Changed UPLOAD_FOLDER from `uploads/` to `static/uploads/` for direct browser access
- **Face Encoding Fix**: Updated VoterFace.set_encoding() to handle tuple conversion with proper tolist() calls
- **Email Service Migration**: Replaced Flask-Mail with Resend email service via Replit connector
  - Integrated ResendEmailService class that uses Replit's connector API for credentials
  - Fallback error handling if Resend credentials unavailable
  - All three email types now use Resend: auth success, auth failure, vote confirmation
- **Image Path Normalization**: Added get_url_path() utility function in utils.py
  - Converts backslashes to forward slashes for consistent URLs
  - Added url_path Jinja2 filter for templates
  - Updated ballot.html, parties.html, candidates.html to use normalized paths
- **Rollback Functionality**: Added /admin/rollback route and dashboard button
  - Clears all votes from database
  - Resets has_voted flag on all voters
  - Allows fresh elections without recreating voter records
- **Dependencies Added**: openpyxl (Excel export), requests (Resend API calls)

### October 1, 2025

### Authentication & Access Control
- **Admin Credentials**: Default login is username `admin` with password `admin123` (bcrypt hashed)
- **Voter Flow**: Removed admin login requirement from voter-facing routes (authentication, ballot, voting, success)
- **Session Gating**: Ballot and voting access controlled via `session['authenticated_voter_id']` instead of admin login

### Face Recognition Enhancements
- **Maximum 5 Images**: Face enrollment now limited to 5 captures per voter for improved accuracy
- **Client-Side Enforcement**: UI restricts capture count and provides feedback during enrollment

### Email Notification System
- **Gmail SMTP**: Configured with app password (trqc subs fkim wbrp)
- **Sender**: electioncomission101@gmail.com
- **Alert Recipient**: mithraa1906@gmail.com (Election Commissioner)
- **Three Email Types**:
  1. **Authentication Success**: Sent to voter after successful face match
  2. **Authentication Failure**: Sent to commissioner and voter with captured photo attachment when face doesn't match
  3. **Vote Confirmation**: Sent to voter with vote details, audit reference, and timestamp

### Voting Flow Alerts
- **Success Path**: Green success alert → Email to voter → Auto-redirect to ballot
- **Fake Face Detection**: Red blinking screen + beep sound → Email with photo to commissioner and voter → Access denied

### Dashboard Routing
- All admin dashboard buttons properly route to management pages:
  - Manage Voters → `/admin/voters`
  - Manage Parties → `/admin/parties`
  - Manage Candidates → `/admin/candidates`

### Database Initialization
- Database tables automatically created via db.create_all() in app context
- PostgreSQL connection via DATABASE_URL environment variable
- Upload directories created on app startup in static/uploads/

## System Architecture

### Frontend Architecture

**Technology Stack**: HTML, CSS (Bootstrap 5), JavaScript (vanilla)

**Key Design Patterns**:
- Template inheritance using Jinja2 base templates for consistent UI across pages
- Responsive design with Bootstrap grid system for mobile and desktop compatibility
- Real-time webcam integration using browser's `getUserMedia` API for face capture
- Modal-based authentication flow for seamless user experience

**Component Structure**:
- Landing page with dual-entry points (Election Commission and Polling System)
- Admin dashboard with statistics cards and navigation to management modules
- Voter authentication flow with webcam-based face verification
- Ballot interface with party symbols and candidate selection

### Backend Architecture

**Framework**: Flask (Python web framework)

**Application Structure**:
- Blueprint-based modular architecture separating concerns:
  - `auth_bp`: Authentication and session management
  - `admin_bp`: Election Commission administrative functions
  - `poll_bp`: Voter authentication and voting operations
  - `results_bp`: Live results and reporting
- Factory pattern for application creation enabling easier testing and configuration
- Service layer pattern isolating business logic (FaceService, EmailService)

**Security Measures**:
- bcrypt password hashing for admin credentials stored in environment variables
- Flask session management for authentication state
- Rate limiting using Flask-Limiter to prevent brute force attacks
- CSRF protection via Flask-WTF forms
- Environment-based configuration separating secrets from code

**Face Recognition Implementation**:
- OpenCV-based face detection using Haar Cascade classifiers
- Custom feature extraction combining histogram analysis and LBP-like descriptors
- Multi-image enrollment (up to 5 images per voter) for improved accuracy
- Euclidean distance-based matching with configurable threshold (default 0.6)
- Liveness detection through face/eye presence validation

**Email Notification System**:
- **Service**: Resend email API via Replit connector integration
- **Credentials**: Fetched dynamically from Replit connector API endpoint
- **Implementation**: ResendEmailService class with fallback error handling
- Asynchronous email sending using threading to prevent blocking
- Three notification types:
  1. Vote confirmation emails to voters with timestamp and reference ID
  2. Authentication success notifications
  3. Security alerts for fake face detection with captured photo attachments
- Multi-recipient support for commissioner alerts
- Graceful degradation if Resend credentials unavailable

### Data Storage

**Database**: PostgreSQL with SQLAlchemy ORM

**Schema Design**:
- `voters`: Core voter registry with personal details, voting status, and email
- `voter_faces`: Face encoding storage with JSON serialization of numpy arrays (one-to-many with voters)
- `parties`: Political party information with symbol image paths
- `candidates`: Candidate records linked to parties
- `votes`: Vote audit trail with anonymized voter references
- `auth_events`: Authentication attempt logging for security monitoring

**Key Architectural Decisions**:
- JSON serialization of face encoding arrays for database storage (avoiding binary blob storage)
- Soft delete pattern support through relationship cascading
- Indexing on voter_id for fast lookup during authentication
- Timestamp tracking (created_at, updated_at) for audit compliance
- Boolean flag (has_voted) for preventing duplicate votes

**Migration Strategy**:
- Flask-Migrate (Alembic) for version-controlled schema changes
- Database connection pooling with pre-ping for connection health checks
- Pool recycling every 300 seconds to prevent stale connections

### External Dependencies

**Third-Party Libraries**:
- **OpenCV (cv2)**: Face detection and image processing
- **NumPy**: Numerical operations for face encoding manipulation
- **Pillow (PIL)**: Image handling and conversion
- **bcrypt**: Secure password hashing
- **Flask-Mail**: Legacy email infrastructure (now unused, kept for compatibility)
- **Flask-Limiter**: API rate limiting
- **Flask-Migrate**: Database migration management
- **Flask-WTF**: CSRF protection and form handling
- **python-dotenv**: Environment variable management
- **openpyxl**: Excel file generation for results export
- **requests**: HTTP client for Resend API integration

**External Services**:
- **Resend Email API** (via Replit Connector):
  - Integration ID: resend==1.0.0
  - Credentials managed automatically by Replit connector
  - API endpoint: https://api.resend.com/emails
  - Sender domain configured in Resend dashboard
  - Commissioner alerts to: mithraa1906@gmail.com

**Database Service**:
- PostgreSQL 16 (configurable via DATABASE_URL environment variable)
- Supports both local and cloud-hosted instances
- Replit provides built-in PostgreSQL option

**Browser APIs**:
- MediaDevices getUserMedia for webcam access
- Canvas API for image capture and base64 encoding
- Web Audio API for alert sound playback

**Configuration Management**:
- Environment variables for sensitive credentials
- .env file for local development
- Replit Secrets for production deployment
- Configurable thresholds (face matching, rate limits)