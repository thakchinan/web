# 🚀 การ Deploy Traffic Congestion Predictor

## ตัวเลือกการ Deploy

### 1. Railway.app (แนะนำ - ฟรี)
Railway.app เป็น platform ที่ง่ายที่สุดสำหรับการ deploy FastAPI

#### ขั้นตอนการ Deploy:

1. **สร้างบัญชี Railway**
   - ไปที่ https://railway.app
   - สมัครสมาชิกด้วย GitHub account

2. **เตรียม Repository**
   ```bash
   # สร้าง Git repository
   git init
   git add .
   git commit -m "Initial commit"
   
   # สร้าง repository บน GitHub
   # จากนั้น push โค้ด
   git remote add origin https://github.com/username/traffic-predictor.git
   git push -u origin main
   ```

3. **Deploy บน Railway**
   - เข้า Railway dashboard
   - กดปุ่ม "New Project"
   - เลือก "Deploy from GitHub repo"
   - เลือก repository ของคุณ
   - Railway จะ auto-detect Python และ deploy

4. **ตั้งค่า Environment Variables (ถ้าจำเป็น)**
   - ใน Railway dashboard > Settings > Variables
   - เพิ่ม variables ที่จำเป็น

### 2. Render.com (ฟรี)

#### ขั้นตอนการ Deploy:

1. **สร้างบัญชี Render**
   - ไปที่ https://render.com
   - สมัครสมาชิกด้วย GitHub

2. **Deploy**
   - กดปุ่ม "New +" > "Web Service"
   - เชื่อมต่อ GitHub repository
   - ตั้งค่า:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
     - **Environment**: Python 3

### 3. Heroku (มีค่าใช้จ่าย)

#### ขั้นตอนการ Deploy:

1. **ติดตั้ง Heroku CLI**
   ```bash
   # Windows
   winget install Heroku.HerokuCLI
   
   # หรือ download จาก https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy**
   ```bash
   # Login
   heroku login
   
   # สร้าง app
   heroku create traffic-predictor-yourname
   
   # Deploy
   git push heroku main
   ```

### 4. PythonAnywhere (ฟรี)

#### ขั้นตอนการ Deploy:

1. **สร้างบัญชี PythonAnywhere**
   - ไปที่ https://pythonanywhere.com
   - สมัครบัญชีฟรี

2. **Upload Files**
   - Upload ไฟล์ทั้งหมดผ่าน web interface
   - หรือใช้ git clone

3. **ตั้งค่า Web App**
   - ไปที่ Web tab
   - สร้าง web app ใหม่
   - เลือก "Manual configuration" > Python 3.10
   - ตั้งค่า WSGI file

## 📁 ไฟล์ที่จำเป็นสำหรับการ Deploy

```
ML_Model_Predictor/
├── app.py                 # ไฟล์หลัก (entry point)
├── simple_rf.py           # ไฟล์เดิม
├── Procfile              # สำหรับ Heroku/Railway
├── runtime.txt           # Python version
├── requirements.txt      # Dependencies
├── templates/
│   └── simple_rf.html    # HTML template
├── static/
│   ├── traffic_style.css # CSS styles
│   └── ...              # ไฟล์อื่นๆ
├── models/
│   └── rf_model.pkl      # ML model
└── DEPLOYMENT.md         # คู่มือนี้
```

## 🔧 การแก้ไขปัญหา

### ปัญหาที่พบบ่อย:

1. **โมเดลไม่โหลด**
   - ตรวจสอบว่าไฟล์ `rf_model.pkl` อยู่ในโฟลเดอร์ `models/`
   - ตรวจสอบ path ในโค้ด

2. **Static files ไม่โหลด**
   - ตรวจสอบการ mount static files
   - ตรวจสอบ path ใน HTML template

3. **Port ไม่ถูกต้อง**
   - ใช้ environment variable `$PORT` สำหรับ hosting platforms
   - ตัวอย่าง: `--port $PORT` หรือ `--port ${PORT}`

### ตัวอย่าง Environment Variables:

```bash
# Railway/Render
PORT=8000

# Heroku (auto-set)
PORT=5000
```

## ✅ การทดสอบหลัง Deploy

1. **ทดสอบ Health Check**
   ```
   GET https://your-app-url.com/health
   ```

2. **ทดสอบหน้าเว็บหลัก**
   ```
   GET https://your-app-url.com/
   ```

3. **ทดสอบ API**
   ```
   POST https://your-app-url.com/predict-traffic
   Content-Type: application/json
   
   {
     "latitude": 13.7563,
     "longitude": 100.5018,
     "density": 50,
     "volume": 1500,
     "capacity": 2000,
     "hour": 8,
     "speed": 45,
     "vc_ratio": 0.75
   }
   ```

## 🎯 ข้อแนะนำ

1. **ใช้ Railway.app** สำหรับเริ่มต้น (ง่ายที่สุด)
2. **Backup โมเดล** ใน cloud storage
3. **Monitor logs** หลัง deploy
4. **ทดสอบการทำงาน** อย่างละเอียด
5. **ตั้งค่า Custom Domain** (ถ้าต้องการ)

---

**หมายเหตุ:** การ deploy อาจใช้เวลาสักครู่ (5-15 นาที) สำหรับการ build และ setup ครั้งแรก

