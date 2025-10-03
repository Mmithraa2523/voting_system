
# Smart Voting System - Setup Instructions

## Prerequisites

- Python 3.11+
- PostgreSQL 16
- Git

## Initial Setup

### 1. Clone and Setup Environment

```bash
# The repository should already be cloned in Replit
# Create your environment configuration
cp .env.example .env
```

### 2. Configure Environment Variables

Edit the `.env` file with your specific configuration:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/smart_voting

# Flask Configuration
SECRET_KEY=your-secret-key-here-make-it-long-and-random

# Email Configuration (Gmail SMTP)
EMAIL_USER=electioncomission101@gmail.com
EMAIL_APP_PASSWORD=your-gmail-app-password-here
EMAIL_FROM="Election Commission <electioncomission101@gmail.com>"

# Admin Configuration
ADMIN_DEFAULT_USER=admin
ADMIN_DEFAULT_PASS_HASH=your-bcrypt-hash-here

# Face Recognition Configuration
FACE_THRESHOLD=0.6

# Alert Configuration
ALERT_RECIPIENT=mithraa1906@gmail.com
```

### 3. Generate Admin Password Hash

To create a secure password hash for admin access:

```python
# Run this in Python to generate password hash
import bcrypt

password = "your_secure_password_here"  # Change this!
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

Copy the output and paste it as the value for `ADMIN_DEFAULT_PASS_HASH` in your `.env` file.

### 4. Database Setup

```bash
# Install dependencies (done automatically in Replit)
# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Gmail App Password Setup

1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password for "Mail"
4. Use this App Password (not your regular Gmail password) in `EMAIL_APP_PASSWORD`

## Default Login Credentials

### Election Commission Access
- **Username:** `admin` (or whatever you set in `ADMIN_DEFAULT_USER`)
- **Password:** Whatever password you used when generating the bcrypt hash
- **Login Type:** Select "Election Commission"

### Polling System Access  
- **Username:** `admin` (same as Election Commission)
- **Password:** Same password as Election Commission
- **Login Type:** Select "Polling System"

## Running the Application

### Development Mode

```bash
# Start the application
python app.py
```

The application will be available at `http://localhost:5000`

### Production Considerations

For production deployment:
1. Set `FLASK_DEBUG=False` in environment
2. Use a production WSGI server
3. Configure proper SSL certificates
4. Use a dedicated database server
5. Implement proper logging and monitoring

## System Features

### For Election Commission (Admin):
- Manage voters and their face recognition data
- Manage political parties and candidates  
- View real-time voting results
- Monitor authentication events and fraud attempts
- Export voting reports

### For Polling System:
- Authenticate voters using face recognition
- Conduct secure voting process
- Record votes with audit trails

## Security Features

1. **Face Recognition Authentication:** Uses OpenCV and face encoding for voter verification
2. **Fraud Detection:** Monitors and alerts on suspicious authentication attempts
3. **Rate Limiting:** Prevents brute force attacks
4. **Audit Trail:** Complete logging of all voting activities
5. **Email Alerts:** Automatic notifications for security events

## Troubleshooting

### Common Issues

1. **Database Connection Error:**
   - Ensure PostgreSQL is running
   - Check DATABASE_URL format
   - Verify database credentials

2. **Face Recognition Not Working:**
   - Ensure OpenCV is properly installed
   - Check camera permissions
   - Verify face encoding data exists

3. **Email Alerts Not Sending:**
   - Verify Gmail App Password is correct
   - Check EMAIL_USER and EMAIL_APP_PASSWORD settings
   - Ensure "Less secure app access" is enabled (if not using App Password)

4. **Login Issues:**
   - Verify ADMIN_DEFAULT_PASS_HASH is correctly generated
   - Check username in ADMIN_DEFAULT_USER
   - Ensure bcrypt hash was generated properly

### Support

For technical support or issues:
1. Check the application logs
2. Verify environment configuration
3. Test database connectivity
4. Review authentication settings

## File Structure

```
├── blueprints/          # Application modules
│   ├── admin/           # Election Commission interface
│   ├── auth/            # Authentication system
│   ├── poll/            # Polling system interface
│   └── results/         # Results and reporting
├── services/            # Business logic services
├── static/              # CSS, JS, images
├── templates/           # HTML templates
├── uploads/             # File uploads (faces, images)
├── models.py            # Database models
├── app.py              # Main application
└── .env                # Environment configuration
```

## Initial Admin Setup Workflow

1. Start the application
2. Navigate to login page
3. Use admin credentials to login as "Election Commission"
4. Add political parties and candidates
5. Register voters with face recognition data
6. Configure polling system access
7. Begin voting process

Remember to keep your `.env` file secure and never commit it to version control!
