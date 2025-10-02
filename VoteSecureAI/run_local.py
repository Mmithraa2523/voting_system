
#!/usr/bin/env python3
"""
Local development runner for Smart Voting System
This script provides a convenient way to run the application locally
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        'DATABASE_URL',
        'SECRET_KEY',
        'EMAIL_USER',
        'EMAIL_APP_PASSWORD',
        'ADMIN_DEFAULT_USER',
        'ADMIN_DEFAULT_PASSWORD'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease check your .env file and ensure all variables are set.")
        print("See .env.example for reference.")
        return False
    
    print("✅ All required environment variables are set!")
    return True

def check_database():
    """Check if database is accessible"""
    try:
        import psycopg2
        database_url = os.environ.get('DATABASE_URL')
        conn = psycopg2.connect(database_url)
        conn.close()
        print("✅ Database connection successful!")
        return True
    except ImportError:
        print("❌ psycopg2 not installed. Run: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please ensure PostgreSQL is running and database exists.")
        return False

def main():
    print("=== Smart Voting System - Local Development ===\n")
    
    # Load environment variables
    if os.path.exists('.env'):
        load_dotenv()
        print("✅ Loaded .env file")
    else:
        print("❌ .env file not found! Please create one using .env.example as template.")
        return False
    
    # Check environment variables
    if not check_environment():
        return False
    
    # Check database connection
    if not check_database():
        return False
    
    # Import and run the app
    try:
        print("\n🚀 Starting Smart Voting System...")
        print("📍 Application will be available at: http://127.0.0.1:5000")
        print("🛑 Press Ctrl+C to stop the server\n")
        
        from app import create_app
        app = create_app()
        app.run(host='127.0.0.1', port=5000, debug=True)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
