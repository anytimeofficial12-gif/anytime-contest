#!/usr/bin/env python3
"""
Local Development Setup Script for ANYTIME Contest Landing Page

This script helps set up the local development environment.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def check_google_credentials():
    """Check if Google credentials file exists"""
    creds_file = "contestdata-472704-c4b8568d4dcb.json"
    if os.path.exists(creds_file):
        print("✅ Google credentials file found")
        return True
    else:
        print("⚠️  Google credentials file not found")
        print("   Please ensure 'contestdata-472704-c4b8568d4dcb.json' is in the project root")
        return False

def create_env_file():
    """Create .env file for local development"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file already exists")
        return
    
    env_content = """# Local Development Environment Variables
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000

# Google Sheets Configuration
GOOGLE_SERVICE_ACCOUNT_FILE=contestdata-472704-c4b8568d4dcb.json
GOOGLE_SPREADSHEET_ID=1tKrJieYsoHpFJzi1bZ5Z28XSzxidikVTXmoyvWxw2VQ
GOOGLE_SHEET_RANGE=Sheet1!A:D
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    print("✅ Created .env file for local development")

def check_config_file():
    """Check if config.js is properly configured"""
    config_file = "config.js"
    if not os.path.exists(config_file):
        print("❌ config.js file not found")
        return False
    
    with open(config_file, 'r') as f:
        content = f.read()
        if "your-backend-url.railway.app" in content:
            print("⚠️  config.js still contains placeholder URL")
            print("   Update API_BASE_URL in config.js for production deployment")
        else:
            print("✅ config.js appears to be configured")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up ANYTIME Contest Landing Page for local development...\n")
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Check Google credentials
    has_creds = check_google_credentials()
    
    # Create .env file
    create_env_file()
    
    # Check config file
    check_config_file()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Ensure Google credentials file is in place")
    print("2. Share your Google Spreadsheet with the service account email")
    print("3. Run the backend: python app.py")
    print("4. Open index.html in your browser or use a local server")
    print("5. Test the form submission")
    
    if not has_creds:
        print("\n⚠️  Important: You need the Google credentials file to use Google Sheets integration")
        print("   Without it, the app will use local storage fallback")
    
    print("\n🔗 Useful commands:")
    print("   python app.py                    # Start backend server")
    print("   python -m http.server 3000       # Start frontend server")
    print("   python setup_local.py            # Run this setup again")

if __name__ == "__main__":
    main()
