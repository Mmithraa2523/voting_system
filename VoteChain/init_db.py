#!/usr/bin/env python3
"""
Database initialization script
Run this script once to create all database tables
"""

import os
from app import create_app
from models import db

def init_database():
    print("=== Smart Voting System - Database Initialization ===\n")
    
    # Create app
    app = create_app()
    
    with app.app_context():
        print(f"Using DATABASE_URL: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
        
        try:
            # Create all tables
            print("\nCreating database tables...")
            db.create_all()
            print("✓ Database tables created successfully!")
            
            # Verify tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n✓ Created {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
            
            print("\n✅ Database initialization complete!")
            print("\nYou can now run the application with: python app.py")
            
        except Exception as e:
            print(f"\n❌ Error initializing database: {e}")
            print("\nPlease check your DATABASE_URL configuration.")
            return False
    
    return True

if __name__ == "__main__":
    init_database()
