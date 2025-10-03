# Smart Voting System

## Overview

A web-based electronic voting application featuring face recognition for secure voter authentication. It provides an Election Commission admin panel for managing voters, parties, and candidates, and a Polling System for authenticated voters to cast votes. The system ensures identity verification via face recognition and utilizes automated email alerts for vote confirmations and security incidents. The project aims to provide a secure and efficient digital voting experience.

## Recent Changes (October 2025)

**Major Face Recognition Upgrade (October 3, 2025):**
- **Upgraded to ResNet-34 based VGG-Face model**: Replaced Facenet512 with VGG-Face (ResNet-34 architecture) producing 4096-D embeddings for superior accuracy
- **Enhanced Quality Assessment**: Added comprehensive pre-encoding quality checks:
  - Brightness validation (rejects too dark/overexposed images)
  - Sharpness testing using Laplacian variance (rejects blurry images)
  - Face size validation (minimum 120x120 pixels)
  - Overall quality scoring with 0.5 minimum threshold
- **Advanced Preprocessing**: Implemented CLAHE (Contrast Limited Adaptive Histogram Equalization) and color denoising for cleaner face inputs
- **Improved Distance Metric**: Switched from Euclidean to Cosine similarity distance for more accurate face matching
- **Stricter Verification Threshold**: Lowered from 0.35 to **0.25** (cosine distance) to prevent false positives - ensures only registered voters can authenticate

**Previous Security & Bug Fixes:**
- Fixed 404 errors for candidate images and party symbols by adding secure `/uploads/` route using `send_from_directory` to prevent path traversal attacks
- Consolidated duplicate upload directories - all files now in `static/uploads/`

**Infrastructure:**
- Installed system dependencies: libGL, mesa, libGLU for OpenCV/OpenGL support
- Created all required upload subdirectories: faces, fraud_attempts, party_symbols, candidate_images
- Database initialized with 6 tables: voters, voter_faces, parties, candidates, votes, auth_events

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
- **Deep Learning Model**: VGG-Face (ResNet-34 architecture) via DeepFace for 4096-D embeddings
- **Quality Gating**: Pre-encoding checks for brightness, sharpness (Laplacian variance), and face size
- **Preprocessing Pipeline**: CLAHE enhancement and color denoising for optimal face inputs
- **OpenCV Integration**: Haar Cascade face detection with alignment support
- **Distance Metric**: Cosine similarity distance with **0.25 threshold** for strict verification
- **Multi-image Enrollment**: Up to 5 images per voter for robust matching
- **Liveness Detection**: AI-powered anti-spoofing (OpenAI/Gemini) to reject photos/screens
- **Fallback Encoding**: Custom LBP+HOG features when DeepFace unavailable

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
- **opencv-python**: Face detection and image processing with OpenCV.
- **deepface**: Deep learning framework for face recognition (VGG-Face/ResNet-34 model).
- **tensorflow**: Deep learning backend for DeepFace.
- **NumPy**: Numerical operations and array handling.
- **Pillow (PIL)**: Image handling and conversion.
- **bcrypt**: Password hashing for admin authentication.
- **Flask-Limiter**: API rate limiting.
- **Flask-Migrate**: Database migration management.
- **Flask-WTF**: CSRF protection and form handling.
- **python-dotenv**: Environment variable management.
- **openpyxl**: Excel file generation for reports.
- **pandas**: Data analysis and reporting.
- **reportlab**: PDF generation for reports.
- **requests**: HTTP client for email API.
- **openai**: AI liveness detection (anti-spoofing).
- **google-generativeai**: Gemini AI for liveness detection fallback.

### System Dependencies (Replit):
- **libGL**: OpenGL library for OpenCV graphical operations.
- **mesa**: OpenGL implementation for rendering support.
- **libGLU**: OpenGL utility library.

### External Services:
- **Resend Email API**: Integrated via Replit connector for email notifications (Auth success, Auth failure, Vote confirmation).
- **PostgreSQL 16**: Database service (configured via `DATABASE_URL`).

### Browser APIs:
- **MediaDevices.getUserMedia**: Webcam access.
- **Canvas API**: Image capture and base64 encoding.
- **Web Audio API**: Alert sound playback.