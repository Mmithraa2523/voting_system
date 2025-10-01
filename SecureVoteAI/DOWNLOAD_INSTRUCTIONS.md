
# Download and Setup Instructions

## Quick Start Guide

### Step 1: Download the Project

1. **Download all files** from this Replit project to your local computer
2. **Create a new folder** on your computer (e.g., `smart-voting-system`)
3. **Save all files** maintaining the same folder structure

### Step 2: Simple Setup

1. **Open Terminal/Command Prompt** in the project folder
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Edit `.env` file with your settings (see LOCAL_SETUP_GUIDE.md for details)

4. **Initialize database** (after setting up PostgreSQL):
   ```bash
   python init_db.py
   ```

5. **Run the application**:
   ```bash
   python run_local.py
   ```

### Step 3: Access the Application

Open your browser and go to: http://127.0.0.1:5000

## Files to Download

Make sure you download all these files and folders:

```
📁 Project Root/
├── 📁 blueprints/
│   ├── 📁 admin/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── 📁 auth/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── 📁 poll/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── 📁 results/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── __init__.py
├── 📁 services/
│   ├── __init__.py
│   ├── email_service.py
│   └── face_service.py
├── 📁 static/
│   ├── 📁 css/
│   │   └── style.css
│   └── 📁 js/
│       └── app.js
├── 📁 templates/
│   ├── 📁 admin/
│   │   ├── candidates.html
│   │   ├── dashboard.html
│   │   ├── enroll_face.html
│   │   ├── parties.html
│   │   └── voters.html
│   ├── 📁 poll/
│   │   ├── auth.html
│   │   ├── ballot.html
│   │   └── success.html
│   ├── base.html
│   ├── index.html
│   └── login.html
├── 📁 uploads/ (create empty folders)
│   ├── 📁 candidate_images/
│   ├── 📁 faces/
│   ├── 📁 fraud_attempts/
│   └── 📁 party_symbols/
├── 📄 app.py
├── 📄 models.py
├── 📄 init_db.py
├── 📄 generate_admin_hash.py
├── 📄 requirements.txt
├── 📄 .env.example
├── 📄 run_local.py
├── 📄 LOCAL_SETUP_GUIDE.md
└── 📄 DOWNLOAD_INSTRUCTIONS.md (this file)
```

## Important Notes

1. **Create upload folders**: Make sure to create the empty upload folders as shown above
2. **PostgreSQL required**: You need to install PostgreSQL database on your system
3. **Gmail setup**: You need a Gmail account with app password for email notifications
4. **Python 3.11+**: Ensure you have Python 3.11 or higher installed

## Need Help?

📖 **Read the detailed guide**: LOCAL_SETUP_GUIDE.md contains step-by-step instructions for everything

🚀 **Quick start**: Use `python run_local.py` to run with built-in environment checks

⚠️ **Troubleshooting**: The LOCAL_SETUP_GUIDE.md includes solutions for common issues

## Default Login

- **Username**: admin
- **Password**: admin123 (or whatever you set when generating the hash)

## System Requirements

- Python 3.11+
- PostgreSQL 16
- Modern web browser with camera support
- 2GB+ RAM
- 1GB free disk space
