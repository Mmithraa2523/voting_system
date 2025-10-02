
# Smart Voting System - Local Setup Guide

## Prerequisites

Before starting, ensure you have the following installed on your system:

1. **Python 3.11 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, make sure to check "Add Python to PATH"

2. **PostgreSQL 16**
   - Download from: https://www.postgresql.org/downloads/
   - Remember the password you set for the `postgres` user during installation

3. **Git** (optional, for cloning)
   - Download from: https://git-scm.com/downloads/

4. **VS Code** (recommended)
   - Download from: https://code.visualstudio.com/
   - Install Python extension for VS Code

## Step 1: Download the Project

### Option A: Download as ZIP
1. Download all project files to a folder (e.g., `smart-voting-system`)
2. Extract if downloaded as ZIP

### Option B: If using Git
```bash
git clone <repository-url>
cd smart-voting-system
```

## Step 2: Install Python Dependencies

1. Open Terminal/Command Prompt in the project directory
2. Install required packages:

```bash
pip install flask==3.1.2
pip install flask-sqlalchemy==3.1.1
pip install flask-migrate==4.1.0
pip install flask-mail==0.10.0
pip install flask-wtf==1.2.2
pip install flask-limiter==3.13
pip install bcrypt==5.0.0
pip install opencv-python==4.11.0.86
pip install numpy==2.3.3
pip install pandas==2.3.2
pip install pillow==11.3.0
pip install psycopg2-binary==2.9.10
pip install python-dotenv==1.1.1
pip install reportlab==4.4.4
pip install pytest==8.4.2
```

Or install all at once:
```bash
pip install flask==3.1.2 flask-sqlalchemy==3.1.1 flask-migrate==4.1.0 flask-mail==0.10.0 flask-wtf==1.2.2 flask-limiter==3.13 bcrypt==5.0.0 opencv-python==4.11.0.86 numpy==2.3.3 pandas==2.3.2 pillow==11.3.0 psycopg2-binary==2.9.10 python-dotenv==1.1.1 reportlab==4.4.4 pytest==8.4.2
```

## Step 3: Database Setup

### 3.1 Start PostgreSQL Service
- **Windows**: PostgreSQL should start automatically. If not, search for "Services" and start "postgresql-x64-16"
- **macOS**: `brew services start postgresql` (if installed via Homebrew)
- **Linux**: `sudo systemctl start postgresql`

### 3.2 Create Database
1. Open Terminal/Command Prompt
2. Connect to PostgreSQL:
```bash
psql -U postgres -h localhost
```
3. Enter your PostgreSQL password when prompted
4. Create the database:
```sql
CREATE DATABASE smart_voting;
\q
```

## Step 4: Configure Environment Variables

Create a `.env` file in the project root directory with the following content:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/smart_voting

# Flask Configuration
SECRET_KEY=your-very-long-secret-key-here-make-it-random-and-secure
FLASK_DEBUG=True

# Email Configuration (Gmail SMTP)
EMAIL_USER=your-gmail-address@gmail.com
EMAIL_APP_PASSWORD=your-gmail-app-password
EMAIL_FROM=Your Name <your-gmail-address@gmail.com>

# Admin Configuration
ADMIN_DEFAULT_USER=admin
ADMIN_DEFAULT_PASSWORD=admin123

# Face Recognition Configuration
FACE_THRESHOLD=0.6

# Alert Configuration (where to send security alerts)
ALERT_RECIPIENT=your-email@gmail.com
```

**Important**: Replace the following values:
- `YOUR_PASSWORD`: Your PostgreSQL password
- `your-gmail-address@gmail.com`: Your Gmail address
- `your-gmail-app-password`: Your Gmail app password (see Step 5)
- `your-email@gmail.com`: Email to receive security alerts
- `admin123`: Change this to your desired admin password

## Step 5: Gmail App Password Setup

To send email notifications, you need a Gmail App Password:

1. **Enable 2-Factor Authentication** on your Google Account:
   - Go to https://myaccount.google.com/security
   - Turn on 2-Step Verification

2. **Generate App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password (remove spaces)
   - Use this as `EMAIL_APP_PASSWORD` in your `.env` file

## Step 6: Initialize Database

Run the database initialization script:

```bash
python init_db.py
```

You should see output confirming that database tables were created successfully.

## Step 7: Run the Application

Start the Flask development server:

```bash
python app.py
```

You should see output similar to:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

## Step 8: Access the Application

Open your web browser and navigate to:
- **Local Access**: http://127.0.0.1:5000
- **Network Access**: http://localhost:5000

## Step 9: Test the System

### 9.1 Login as Admin
1. Click "Election Commission"
2. Username: `admin`
3. Password: `admin123`

### 10.2 Set Up Voting System
1. Add political parties in "Manage Parties"
2. Add candidates in "Manage Candidates"
3. Add voters in "Manage Voters"
4. Enroll face recognition for voters

### 10.3 Test Voting
1. Go back to homepage
2. Click "Polling System"
3. Login with admin credentials
4. Test voter authentication and voting

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Error
**Error**: `psycopg2.OperationalError: could not connect to server`

**Solutions**:
- Ensure PostgreSQL service is running
- Check your DATABASE_URL in `.env` file
- Verify your PostgreSQL password
- Try connecting manually: `psql -U postgres -h localhost`

#### 2. Import Errors
**Error**: `ModuleNotFoundError: No module named '...'`

**Solutions**:
- Ensure all dependencies are installed: `pip list`
- Reinstall missing packages
- Check Python version: `python --version`

#### 3. OpenCV Issues
**Error**: Face detection not working

**Solutions**:
- Reinstall OpenCV: `pip uninstall opencv-python && pip install opencv-python`
- On Linux, install system dependencies:
  ```bash
  sudo apt-get update
  sudo apt-get install python3-opencv
  ```

#### 4. Email Not Sending
**Error**: Email notifications not working

**Solutions**:
- Verify Gmail App Password is correct
- Check 2-Factor Authentication is enabled
- Test with a simple email first
- Check firewall/antivirus blocking SMTP

#### 5. Port Already in Use
**Error**: `Address already in use`

**Solutions**:
- Kill existing process: `lsof -ti:5000 | xargs kill -9` (Mac/Linux)
- Use different port: Edit `app.py` and change `port=5000` to `port=5001`

#### 6. Webcam Access Issues
**Error**: Camera not working in browser

**Solutions**:
- Use HTTPS (required for camera access)
- Grant camera permissions in browser
- Try different browser (Chrome recommended)
- Check camera is not used by other applications

## Development Tips

### VS Code Setup
1. Install Python extension
2. Set Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Install recommended extensions:
   - Python
   - Python Docstring Generator
   - GitLens (if using Git)

### Database Management
- **View data**: Use pgAdmin (comes with PostgreSQL) or DBeaver
- **Reset database**: Drop and recreate the `smart_voting` database
- **Backup**: `pg_dump -U postgres smart_voting > backup.sql`
- **Restore**: `psql -U postgres smart_voting < backup.sql`

### Security Considerations
- Change default admin password immediately
- Use strong SECRET_KEY in production
- Keep Gmail App Password secure
- Regular backup of database
- Use HTTPS in production

## File Structure

```
smart-voting-system/
├── blueprints/          # Application modules
│   ├── admin/           # Admin interface
│   ├── auth/            # Authentication
│   ├── poll/            # Voting system
│   └── results/         # Results display
├── services/            # Business logic
│   ├── email_service.py # Email functionality
│   └── face_service.py  # Face recognition
├── static/              # CSS, JS files
├── templates/           # HTML templates
├── uploads/             # File uploads
├── .env                 # Environment variables (you create this)
├── app.py              # Main application
├── init_db.py          # Database setup
├── models.py           # Database models
└── generate_admin_hash.py # Password generator
```

## Production Deployment

For production deployment, consider:
- Use proper WSGI server (Gunicorn, uWSGI)
- Set up reverse proxy (Nginx)
- Use environment variables instead of `.env` file
- Enable SSL/HTTPS
- Use production database server
- Implement proper logging
- Set up monitoring and backups

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are correctly installed
3. Ensure PostgreSQL is running and accessible
4. Check the console output for error messages
5. Verify your `.env` file configuration

Remember to keep your credentials secure and never commit the `.env` file to version control!
