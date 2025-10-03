# Smart Voting System

## Overview

A web-based electronic voting application featuring face recognition for secure voter authentication. It provides an Election Commission admin panel for managing voters, parties, and candidates, and a Polling System for authenticated voters to cast votes. The system ensures identity verification via face recognition and utilizes automated email alerts for vote confirmations and security incidents. The project aims to provide a secure and efficient digital voting experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack**: HTML, CSS (Bootstrap 5), JavaScript (vanilla)

**Key Design Patterns**:
- Jinja2 template inheritance for consistent UI.
- Responsive design using Bootstrap.
- Real-time webcam integration via `getUserMedia` for face capture.
- Modal-based authentication flow.

### Backend Architecture

**Framework**: Flask (Python web framework)

**Application Structure**:
- Modular blueprint-based architecture (`auth_bp`, `admin_bp`, `poll_bp`, `results_bp`).
- Factory pattern for application creation.
- Service layer pattern for business logic (e.g., `FaceService`, `EmailService`).

**Security Measures**:
- bcrypt for admin password hashing.
- Flask session management for authentication state.
- CSRF protection via Flask-WTF.
- Environment-based configuration for secrets.

**Face Recognition Implementation**:
- OpenCV for face detection (Haar Cascade classifiers).
- Custom 128-D feature extraction combining histogram analysis and LBP-like descriptors.
- Multi-image enrollment (up to 5 images per voter).
- Euclidean distance-based matching with configurable threshold.
- Basic liveness detection via face/eye presence validation.

**Email Notification System**:
- Resend email API integration via Replit connector.
- Asynchronous email sending using threading.
- Notifications for vote confirmation, authentication success, and security alerts (fake face detection).

### Data Storage

**Database**: PostgreSQL with SQLAlchemy ORM

**Schema Design**:
- `voters`: Voter registry, voting status, email.
- `voter_faces`: JSON serialized 128-D face encodings.
- `parties`: Political party information with symbol image paths.
- `candidates`: Candidate records linked to parties.
- `votes`: Vote audit trail with anonymized voter references.
- `auth_events`: Authentication attempt logs.

**Key Architectural Decisions**:
- JSON serialization of face encodings for database storage.
- Cascade delete relationships for data integrity.
- Indexing on `voter_id` for performance.
- Timestamp tracking for audit.
- `has_voted` flag to prevent duplicate votes.

## External Dependencies

### Third-Party Libraries:
- **OpenCV (cv2)**: Face detection and image processing.
- **NumPy**: Numerical operations.
- **Pillow (PIL)**: Image handling.
- **bcrypt**: Password hashing.
- **Flask-Limiter**: API rate limiting.
- **Flask-Migrate**: Database migration management.
- **Flask-WTF**: CSRF protection and form handling.
- **python-dotenv**: Environment variable management.
- **openpyxl**: Excel file generation.
- **requests**: HTTP client for Resend API.

### External Services:
- **Resend Email API**: Integrated via Replit connector for email notifications (Auth success, Auth failure, Vote confirmation).
- **PostgreSQL 16**: Database service (configured via `DATABASE_URL`).

### Browser APIs:
- **MediaDevices.getUserMedia**: Webcam access.
- **Canvas API**: Image capture and base64 encoding.
- **Web Audio API**: Alert sound playback.