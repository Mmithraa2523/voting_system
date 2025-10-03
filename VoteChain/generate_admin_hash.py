
#!/usr/bin/env python3
"""
Script to generate bcrypt hash for admin password
Run this script and copy the output to your .env file as ADMIN_DEFAULT_PASS_HASH
"""

import bcrypt
import getpass

def generate_password_hash():
    print("=== Smart Voting System - Admin Password Hash Generator ===\n")
    
    # Get password from user
    password = getpass.getpass("Enter admin password: ")
    confirm_password = getpass.getpass("Confirm admin password: ")
    
    if password != confirm_password:
        print("❌ Passwords don't match! Please try again.")
        return
    
    if len(password) < 8:
        print("❌ Password should be at least 8 characters long.")
        return
    
    # Generate hash
    print("\n🔐 Generating secure hash...")
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hash_string = hashed.decode('utf-8')
    
    print(f"\n✅ Password hash generated successfully!")
    print(f"\n📝 Copy this hash to your .env file:")
    print(f"ADMIN_DEFAULT_PASS_HASH={hash_string}")
    
    # Verify the hash works
    print(f"\n🧪 Verifying hash...")
    if bcrypt.checkpw(password.encode('utf-8'), hashed):
        print("✅ Hash verification successful!")
    else:
        print("❌ Hash verification failed!")
    
    print(f"\n💡 Your admin login credentials will be:")
    print(f"Username: admin (or whatever you set in ADMIN_DEFAULT_USER)")
    print(f"Password: [the password you just entered]")

if __name__ == "__main__":
    try:
        generate_password_hash()
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
