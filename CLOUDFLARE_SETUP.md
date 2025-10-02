# 🌐 Deploy FastAPI ด้วย Cloudflare Tunnel

## 📋 **ขั้นตอนการติดตั้งและ Deploy**

### **1. ติดตั้ง cloudflared**

#### **Windows:**
```powershell
# ดาวน์โหลด cloudflared
winget install --id Cloudflare.cloudflared
```

หรือดาวน์โหลดจาก: https://github.com/cloudflare/cloudflared/releases

---

### **2. Login เข้า Cloudflare**

```bash
cloudflared tunnel login
```

- จะเปิดเบราว์เซอร์ให้คุณ login
- เลือก domain ที่ต้องการใช้

---

### **3. สร้าง Tunnel**

```bash
cloudflared tunnel create traffic-predictor
```

- จะได้ **Tunnel ID** และไฟล์ credential

---

### **4. สร้างไฟล์ config.yml**

สร้างไฟล์ `config.yml` ในโฟลเดอร์ `~/.cloudflared/` (หรือ `C:\Users\<username>\.cloudflared\` บน Windows):

```yaml
tunnel: <TUNNEL_ID>
credentials-file: C:\Users\<username>\.cloudflared\<TUNNEL_ID>.json

ingress:
  - hostname: traffic.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404
```

**แทนที่:**
- `<TUNNEL_ID>` ด้วย Tunnel ID ที่ได้จากขั้นตอนที่ 3
- `traffic.yourdomain.com` ด้วย subdomain ที่คุณต้องการ
- `<username>` ด้วยชื่อ user ของคุณ

---

### **5. สร้าง DNS Record**

```bash
cloudflared tunnel route dns traffic-predictor traffic.yourdomain.com
```

**แทนที่:**
- `traffic.yourdomain.com` ด้วย subdomain ที่คุณต้องการ

---

### **6. รัน FastAPI Server**

เปิด Terminal แรก:

```bash
cd "C:\Users\thakc\Downloads\web machine\web\ML_Model_Predictor"
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

---

### **7. รัน Cloudflare Tunnel**

เปิด Terminal ที่สอง:

```bash
cloudflared tunnel run traffic-predictor
```

---

## 🎉 **เสร็จสิ้น!**

ตอนนี้เว็บของคุณจะสามารถเข้าถึงได้จาก:
- `https://traffic.yourdomain.com`

---

## 🔧 **คำสั่งที่มีประโยชน์**

### **ดู Tunnel ทั้งหมด:**
```bash
cloudflared tunnel list
```

### **ดูข้อมูล Tunnel:**
```bash
cloudflared tunnel info traffic-predictor
```

### **ลบ Tunnel:**
```bash
cloudflared tunnel delete traffic-predictor
```

### **รัน Tunnel แบบ Quick (ไม่ต้อง config):**
```bash
cloudflared tunnel --url http://localhost:8000
```

- จะได้ URL แบบสุ่ม เช่น `https://random-name.trycloudflare.com`
- ใช้สำหรับทดสอบเท่านั้น (URL จะเปลี่ยนทุกครั้งที่รัน)

---

## 🚀 **Quick Start (สำหรับทดสอบ)**

ถ้าต้องการทดสอบเร็วๆ โดยไม่ต้อง config:

### **Terminal 1 - รัน FastAPI:**
```bash
cd "C:\Users\thakc\Downloads\web machine\web\ML_Model_Predictor"
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### **Terminal 2 - รัน Cloudflare Tunnel:**
```bash
cloudflared tunnel --url http://localhost:8000
```

จะได้ URL แบบสุ่มทันที เช่น:
```
https://random-name.trycloudflare.com
```

---

## 📝 **หมายเหตุ:**

- **Quick Tunnel** (ไม่ต้อง login) - URL จะเปลี่ยนทุกครั้ง
- **Named Tunnel** (ต้อง login) - URL คงที่, ใช้ได้นาน

---

## 🛡️ **ข้อดีของ Cloudflare Tunnel:**

✅ **ไม่ต้องเปิด Port** - ไม่ต้องเปิด port 8000 บน router
✅ **HTTPS ฟรี** - SSL/TLS certificate อัตโนมัติ
✅ **ปลอดภัย** - DDoS protection จาก Cloudflare
✅ **ง่าย** - ไม่ต้อง config firewall
✅ **เร็ว** - CDN ระดับโลก

---

## 🎯 **ตัวอย่างการใช้งาน:**

### **1. ทดสอบเร็วๆ (Quick Tunnel):**
```bash
# Terminal 1
python -m uvicorn app:app --host 0.0.0.0 --port 8000

# Terminal 2
cloudflared tunnel --url http://localhost:8000
```

### **2. Production (Named Tunnel):**
```bash
# ครั้งแรก (setup)
cloudflared tunnel login
cloudflared tunnel create traffic-predictor
cloudflared tunnel route dns traffic-predictor traffic.yourdomain.com

# ทุกครั้งที่รัน
# Terminal 1
python -m uvicorn app:app --host 0.0.0.0 --port 8000

# Terminal 2
cloudflared tunnel run traffic-predictor
```

---

## 🔍 **Troubleshooting:**

### **ไม่มี domain:**
- ใช้ Quick Tunnel (`cloudflared tunnel --url http://localhost:8000`)
- หรือซื้อ domain ฟรีที่ Freenom.com

### **Tunnel ไม่ทำงาน:**
```bash
# ตรวจสอบ FastAPI ทำงานหรือไม่
curl http://localhost:8000

# ตรวจสอบ cloudflared version
cloudflared version

# อัปเดต cloudflared
winget upgrade --id Cloudflare.cloudflared
```

### **Permission Error:**
- รัน PowerShell หรือ Command Prompt แบบ Administrator

---

## 🎊 **พร้อมใช้งาน!**

ตอนนี้คุณสามารถแชร์ URL ให้คนอื่นเข้าใช้งานได้แล้ว! 🚀

