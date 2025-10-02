# 🚀 การรัน FastAPI บนเครื่องของคุณ + Cloudflare Tunnel

## 📋 **ขั้นตอนการติดตั้ง**

### **1. ติดตั้ง Python Packages**

```bash
cd "C:\Users\thakc\Downloads\web machine\web\ML_Model_Predictor"
pip install -r requirements.txt
```

---

### **2. ติดตั้ง Cloudflare Tunnel (cloudflared)**

#### **Windows (ใช้ winget):**
```powershell
winget install --id Cloudflare.cloudflared
```

#### **Windows (ดาวน์โหลดโดยตรง):**
1. ไปที่: https://github.com/cloudflare/cloudflared/releases
2. ดาวน์โหลด `cloudflared-windows-amd64.exe`
3. เปลี่ยนชื่อเป็น `cloudflared.exe`
4. ย้ายไปไว้ที่ `C:\Windows\System32\`

---

## 🎯 **วิธีการรัน (แบบง่าย)**

### **วิธีที่ 1: ใช้ไฟล์ .bat (แนะนำ)**

#### **Terminal 1 - รัน FastAPI Server:**
1. Double-click `start_server.bat`
2. รอจนกว่าจะขึ้น "Application startup complete"

#### **Terminal 2 - รัน Cloudflare Tunnel:**
1. Double-click `start_cloudflare.bat`
2. คัดลอก URL ที่ได้ เช่น `https://random-name.trycloudflare.com`
3. เปิดเบราว์เซอร์และเข้าไปที่ URL นั้น

---

### **วิธีที่ 2: ใช้ Command Line**

#### **Terminal 1 - รัน FastAPI Server:**
```bash
cd "C:\Users\thakc\Downloads\web machine\web\ML_Model_Predictor"
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

#### **Terminal 2 - รัน Cloudflare Tunnel:**
```bash
cloudflared tunnel --url http://localhost:8000
```

---

## 🌐 **เข้าถึงเว็บของคุณ**

### **Local (บนเครื่องของคุณเท่านั้น):**
- http://localhost:8000
- http://127.0.0.1:8000

### **Public (ทุกคนเข้าถึงได้ผ่านอินเทอร์เน็ต):**
- https://random-name.trycloudflare.com (จะได้จาก cloudflared)

---

## 📚 **API Endpoints**

### **หน้าแรก:**
```
GET /
```

### **ตรวจสอบสถานะ:**
```
GET /health
```

### **ทำนายการจราจร:**
```
POST /predict-traffic
Content-Type: application/json

{
  "hour": 8,
  "day_of_week": 1,
  "temperature": 30,
  "humidity": 70,
  "rainfall": 0,
  "vehicle_count": 150,
  "speed": 40
}
```

### **API Documentation (Swagger UI):**
```
GET /docs
```

### **Alternative API Documentation (ReDoc):**
```
GET /redoc
```

---

## 🔧 **คำสั่งที่มีประโยชน์**

### **ตรวจสอบว่า FastAPI ทำงานหรือไม่:**
```bash
curl http://localhost:8000/health
```

### **ดูข้อมูลโมเดล:**
```bash
curl http://localhost:8000/
```

### **ทดสอบ API:**
```bash
curl -X POST http://localhost:8000/predict-traffic ^
  -H "Content-Type: application/json" ^
  -d "{\"hour\":8,\"day_of_week\":1,\"temperature\":30}"
```

---

## 🛡️ **ข้อดีของ Cloudflare Tunnel:**

✅ **ไม่ต้องเปิด Port** - ไม่ต้องแก้ไข router/firewall
✅ **HTTPS อัตโนมัติ** - มี SSL certificate ให้ฟรี
✅ **ปลอดภัย** - มี DDoS protection
✅ **แชร์ง่าย** - ส่ง URL ให้เพื่อนได้เลย
✅ **ไม่ต้อง Domain** - ได้ subdomain ฟรี

---

## 🔍 **Troubleshooting**

### **ปัญหา: uvicorn: command not found**
```bash
# ติดตั้งใหม่
pip install uvicorn

# หรือใช้ python -m
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### **ปัญหา: cloudflared: command not found**
```bash
# ติดตั้งใหม่
winget install --id Cloudflare.cloudflared

# หรือดาวน์โหลดจาก GitHub
# https://github.com/cloudflare/cloudflared/releases
```

### **ปัญหา: Port 8000 is already in use**
```bash
# ใช้ port อื่น
python -m uvicorn app:app --host 0.0.0.0 --port 8001

# อัปเดต cloudflared URL
cloudflared tunnel --url http://localhost:8001
```

### **ปัญหา: Module not found**
```bash
# ติดตั้ง dependencies ใหม่
pip install -r requirements.txt

# หรือติดตั้งทีละตัว
pip install fastapi uvicorn joblib pandas scikit-learn numpy
```

### **ปัญหา: Model ไม่โหลด**
```bash
# ตรวจสอบว่าไฟล์โมเดลอยู่ที่ถูกต้อง
dir models\rf_model.pkl

# ตรวจสอบ error log
python app.py
```

---

## 📝 **หมายเหตุ:**

- **URL จาก Cloudflare จะเปลี่ยนทุกครั้งที่รัน** (Quick Tunnel)
- ถ้าต้องการ URL ถาวร ให้ใช้ Named Tunnel (ดูใน `CLOUDFLARE_SETUP.md`)
- FastAPI จะ auto-reload เมื่อคุณแก้ไขโค้ด (เพราะมี `--reload` flag)

---

## 🎊 **ตัวอย่างการใช้งาน**

### **1. เปิด Terminal 1:**
```bash
cd "C:\Users\thakc\Downloads\web machine\web\ML_Model_Predictor"
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
✅ โหลดโมเดล Traffic Jam (Random Forest) สำเร็จ
✅ โหลดโมเดล Day Type (Random Forest) สำเร็จ
INFO:     Application startup complete.
```

### **2. เปิด Terminal 2:**
```bash
cloudflared tunnel --url http://localhost:8000
```

**Output:**
```
2024-10-02T10:00:00Z INF Thank you for trying Cloudflare Tunnel. Doing so, without a Cloudflare account, is a quick way to experiment and try it out. However, be aware that these account-less Tunnels have no uptime guarantee. If you intend to use Tunnels in production you should use a pre-created named tunnel by following: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps
2024-10-02T10:00:01Z INF Requesting new quick Tunnel on trycloudflare.com...
2024-10-02T10:00:02Z INF +--------------------------------------------------------------------------------------------+
2024-10-02T10:00:02Z INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
2024-10-02T10:00:02Z INF |  https://random-name-1234.trycloudflare.com                                                 |
2024-10-02T10:00:02Z INF +--------------------------------------------------------------------------------------------+
```

### **3. เปิดเบราว์เซอร์:**
ไปที่ `https://random-name-1234.trycloudflare.com`

---

## 🚀 **พร้อมใช้งาน!**

ตอนนี้คุณสามารถ:
- ✅ รัน FastAPI บนเครื่องของคุณ
- ✅ แชร์ URL ให้คนอื่นเข้าถึงได้
- ✅ ทดสอบ API ผ่าน Swagger UI
- ✅ Deploy โดยไม่ต้องเสียเงิน!

