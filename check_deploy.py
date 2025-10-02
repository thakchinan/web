#!/usr/bin/env python3
"""
Traffic Congestion Predictor - Deployment Check Script
"""

import os
import subprocess
import sys

def check_requirements():
    """Check required files for deployment"""
    required_files = [
        "app.py",
        "requirements.txt",
        "Procfile",
        "runtime.txt",
        "models/rf_model.pkl",
        "templates/simple_rf.html",
        "static/traffic_style.css"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("All files ready for deployment")
    return True

def check_git_status():
    """Check Git repository status"""
    try:
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode != 0:
            print("No Git repository found")
            return False
        
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.stdout.strip():
            print("Uncommitted files:")
            print(result.stdout)
            return False
        
        print("Git repository ready for deployment")
        return True
        
    except FileNotFoundError:
        print("Git not installed")
        return False

def show_deployment_instructions():
    """Show deployment instructions"""
    instructions = """
DEPLOYMENT INSTRUCTIONS for Traffic Congestion Predictor

OPTION 1 - Railway.app (Recommended - Free):
1. Go to https://railway.app
2. Sign up with GitHub account
3. Click "New Project" > "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-deploy

OPTION 2 - Render.com (Free):
1. Go to https://render.com
2. Sign up with GitHub account
3. Click "New +" > "Web Service"
4. Connect GitHub repository
5. Set Build Command: pip install -r requirements.txt
6. Set Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT

OPTION 3 - Heroku (Paid):
1. Install Heroku CLI
2. heroku login
3. heroku create traffic-predictor-yourname
4. git push heroku main

REQUIRED FILES:
   - app.py (entry point)
   - requirements.txt (dependencies)
   - Procfile (startup command)
   - runtime.txt (Python version)
   - models/rf_model.pkl (ML model)
   - templates/simple_rf.html (web template)
   - static/traffic_style.css (styles)

TROUBLESHOOTING:
   - Check logs in hosting platform
   - Test health check: /health
   - Check static files path
   - Check model file path

Read more details in DEPLOYMENT.md
"""
    print(instructions)

def main():
    print("Traffic Congestion Predictor - Deployment Checker")
    print("=" * 60)
    
    # Check required files
    if not check_requirements():
        print("\nPlease prepare missing files before deployment")
        return
    
    # Check Git status
    if not check_git_status():
        print("\nPlease commit all files before deployment:")
        print("   git add .")
        print("   git commit -m 'Ready for deployment'")
        return
    
    # Show deployment instructions
    show_deployment_instructions()
    
    print("\nReady for deployment!")
    print("Recommended: Use Railway.app for easiest deployment")

if __name__ == "__main__":
    main()
