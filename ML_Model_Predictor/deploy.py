#!/usr/bin/env python3
"""
🚀 Traffic Congestion Predictor - Deployment Helper Script
ช่วยในการ deploy แอปพลิเคชันไปยัง hosting platforms
"""

import os
import subprocess
import sys
import json

def check_requirements():
    """ตรวจสอบไฟล์ที่จำเป็นสำหรับการ deploy"""
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
    """ตรวจสอบสถานะ Git repository"""
    try:
        # ตรวจสอบว่าเป็น Git repository หรือไม่
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  ไม่พบ Git repository")
            return False
        
        # ตรวจสอบไฟล์ที่ยังไม่ได้ commit
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️  มีไฟล์ที่ยังไม่ได้ commit:")
            print(result.stdout)
            return False
        
        print("✅ Git repository พร้อมสำหรับการ deploy")
        return True
        
    except FileNotFoundError:
        print("❌ Git ไม่ได้ติดตั้งในระบบ")
        return False

def create_gitignore():
    """สร้างไฟล์ .gitignore"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Environment variables
.env
.env.local

# Model files (ถ้าไฟล์ใหญ่เกินไป)
# models/*.pkl
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    print("✅ สร้างไฟล์ .gitignore เรียบร้อย")

def init_git_repo():
    """เริ่มต้น Git repository"""
    try:
        # ตรวจสอบว่าเป็น Git repository หรือไม่
        subprocess.run(["git", "status"], capture_output=True, check=True)
        print("✅ Git repository มีอยู่แล้ว")
    except subprocess.CalledProcessError:
        print("🔄 เริ่มต้น Git repository...")
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit - Traffic Congestion Predictor"], check=True)
        print("✅ สร้าง Git repository เรียบร้อย")

def show_deployment_instructions():
    """แสดงคำแนะนำการ deploy"""
    instructions = """
🚀 คำแนะนำการ Deploy Traffic Congestion Predictor

📋 ขั้นตอนการ Deploy:

1️⃣  Railway.app (แนะนำ - ฟรี):
   • ไปที่ https://railway.app
   • สมัครสมาชิกด้วย GitHub
   • กด "New Project" > "Deploy from GitHub repo"
   • เลือก repository ของคุณ
   • Railway จะ auto-deploy

2️⃣  Render.com (ฟรี):
   • ไปที่ https://render.com
   • สมัครสมาชิกด้วย GitHub
   • กด "New +" > "Web Service"
   • เชื่อมต่อ GitHub repository
   • ตั้งค่า Build Command: pip install -r requirements.txt
   • ตั้งค่า Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT

3️⃣  Heroku (มีค่าใช้จ่าย):
   • ติดตั้ง Heroku CLI
   • heroku login
   • heroku create traffic-predictor-yourname
   • git push heroku main

📁 ไฟล์ที่จำเป็น:
   ✅ app.py (entry point)
   ✅ requirements.txt (dependencies)
   ✅ Procfile (startup command)
   ✅ runtime.txt (Python version)
   ✅ models/rf_model.pkl (ML model)
   ✅ templates/simple_rf.html (web template)
   ✅ static/traffic_style.css (styles)

🔧 การแก้ไขปัญหา:
   • ตรวจสอบ logs ใน hosting platform
   • ทดสอบ health check: /health
   • ตรวจสอบ static files path
   • ตรวจสอบ model file path

📖 อ่านรายละเอียดเพิ่มเติมใน DEPLOYMENT.md
"""
    print(instructions)

def main():
    print("Traffic Congestion Predictor - Deployment Helper")
    print("=" * 60)
    
    # ตรวจสอบไฟล์ที่จำเป็น
    if not check_requirements():
        print("\n❌ กรุณาเตรียมไฟล์ที่ขาดหายไปก่อนทำการ deploy")
        return
    
    # สร้าง .gitignore
    if not os.path.exists(".gitignore"):
        create_gitignore()
    
    # เริ่มต้น Git repository
    init_git_repo()
    
    # ตรวจสอบสถานะ Git
    if not check_git_status():
        print("\n⚠️  กรุณา commit ไฟล์ทั้งหมดก่อนทำการ deploy:")
        print("   git add .")
        print("   git commit -m 'Ready for deployment'")
        return
    
    # แสดงคำแนะนำการ deploy
    show_deployment_instructions()
    
    print("\n🎉 พร้อมสำหรับการ deploy แล้ว!")
    print("💡 แนะนำให้ใช้ Railway.app สำหรับการเริ่มต้น")

if __name__ == "__main__":
    main()
