import os
import sys
import json

# Fix numpy._core issue BEFORE importing numpy
try:
    import numpy._core
except ImportError:
    try:
        import numpy.core as _core
        sys.modules['numpy._core'] = _core
    except ImportError:
        pass

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print(f"NumPy version: {np.__version__}")

# ===== FastAPI setup =====
app = FastAPI(title="Traffic Congestion Predictor", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Static files and templates =====
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ===== Traffic Labels =====
traffic_labels = {
    "0": "การจราจรไม่ติด (Free Flow)",
    "1": "การจราจรติด (Congested)"
}

day_type_labels = {
    "0": "วันทำงาน (Weekday)",
    "1": "วันหยุด (Weekend/Holiday)"
}

# ===== Load Models =====
jam_model = None
day_model = None

try:
    jam_model = joblib.load("models/rf_model.pkl")
    print("[OK] Traffic Jam model loaded successfully")
except Exception as e:
    print(f"[ERROR] Cannot load Traffic Jam model: {e}")
    jam_model = None

try:
    day_model = joblib.load("models/rf_model.pkl")
    print("[OK] Day Type model loaded successfully")
except Exception as e:
    print(f"[ERROR] Cannot load Day Type model: {e}")
    day_model = None

# ===== Feature Engineering =====
def create_jam_features(data):
    """สร้างฟีเจอร์สำหรับการทำนายการจราจรติด/ไม่ติด"""
    # Required features: latitude, longitude, density, volume, capacity, hour, speed, v/c
    latitude = float(data.get("latitude", 13.7563))
    longitude = float(data.get("longitude", 100.5018))
    density = float(data.get("density", 50))
    volume = float(data.get("volume", 1500))
    capacity = float(data.get("capacity", 2000))
    hour = int(data.get("hour", 12))
    speed = float(data.get("speed", 45))
    vc_ratio = float(data.get("vc_ratio", 0.75))
    
    # Create feature array matching the model's expected format
    features = [
        latitude, longitude, density, volume, capacity, 
        hour, speed, vc_ratio
    ]
    
    return np.array(features).reshape(1, -1)

def create_day_features(data):
    """สร้างฟีเจอร์สำหรับการทำนายประเภทวัน"""
    # Use the same features as jam model
    return create_jam_features(data)

# ===== API Endpoints =====
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """หน้าแรกของแอปพลิเคชัน"""
    return templates.TemplateResponse("simple_rf.html", {"request": request})

@app.get("/health")
def health():
    """ตรวจสอบสถานะของ API"""
    return {
        "status": "ok", 
        "jam_model": "loaded" if jam_model is not None else "not_loaded",
        "day_model": "loaded" if day_model is not None else "not_loaded",
        "numpy_version": np.__version__
    }

@app.post("/predict-traffic")
async def predict_traffic(data: dict):
    """ทำนายการจราจรติด/ไม่ติด"""
    try:
        if jam_model is None:
            return {"error": "โมเดลยังไม่พร้อมใช้งาน", "status": "error"}
        
        # สร้างฟีเจอร์
        features = create_jam_features(data)
        
        # ทำนาย
        prediction = jam_model.predict(features)[0]
        probability = jam_model.predict_proba(features)[0]
        
        # แปลงผลลัพธ์
        result = {
            "prediction": int(prediction),
            "label": traffic_labels[str(prediction)],
            "confidence": float(max(probability)),
            "probabilities": {
                "free_flow": float(probability[0]),
                "congested": float(probability[1])
            },
            "status": "success"
        }
        
        return result
        
    except Exception as e:
        return {"error": f"เกิดข้อผิดพลาด: {str(e)}", "status": "error"}

@app.post("/predict/jam")
async def predict_traffic_jam(data: dict):
    """ทำนายการจราจรติด/ไม่ติด (Alternative endpoint)"""
    return await predict_traffic(data)

@app.post("/predict/day")
async def predict_day_type(data: dict):
    """ทำนายประเภทวัน (วันทำงาน/วันหยุด)"""
    try:
        if day_model is None:
            return {"error": "โมเดลยังไม่พร้อมใช้งาน", "status": "error"}
        
        # สร้างฟีเจอร์
        features = create_day_features(data)
        
        # ทำนาย
        prediction = day_model.predict(features)[0]
        probability = day_model.predict_proba(features)[0]
        
        # แปลงผลลัพธ์
        result = {
            "prediction": int(prediction),
            "label": day_type_labels[str(prediction)],
            "confidence": float(max(probability)),
            "probabilities": {
                "weekday": float(probability[0]),
                "weekend": float(probability[1])
            },
            "status": "success"
        }
        
        return result
        
    except Exception as e:
        return {"error": f"เกิดข้อผิดพลาด: {str(e)}", "status": "error"}

@app.post("/predict/both")
async def predict_both(data: dict):
    """ทำนายทั้งการจราจรติดและประเภทวัน"""
    try:
        jam_result = await predict_traffic(data)
        day_result = await predict_day_type(data)
        
        return {
            "traffic_jam": jam_result,
            "day_type": day_result,
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"เกิดข้อผิดพลาด: {str(e)}", "status": "error"}

# ===== Additional endpoints =====
@app.get("/api/info")
def api_info():
    """ข้อมูล API"""
    return {
        "name": "Traffic Congestion Predictor API",
        "version": "1.0.0",
        "description": "API สำหรับทำนายการจราจรติดและประเภทวัน",
        "endpoints": {
            "health": {
                "method": "GET",
                "path": "/health",
                "description": "ตรวจสอบสถานะของ API"
            },
            "predict_traffic": {
                "method": "POST",
                "path": "/predict-traffic",
                "description": "ทำนายการจราจรติด/ไม่ติด"
            },
            "predict_jam": {
                "method": "POST",
                "path": "/predict/jam",
                "description": "ทำนายการจราจรติด/ไม่ติด (Alternative)"
            },
            "predict_day": {
                "method": "POST",
                "path": "/predict/day",
                "description": "ทำนายประเภทวัน"
            },
            "predict_both": {
                "method": "POST",
                "path": "/predict/both",
                "description": "ทำนายทั้งการจราจรติดและประเภทวัน"
            }
        },
        "example_request": {
            "hour": 8,
            "day_of_week": 1,
            "temperature": 30,
            "humidity": 70,
            "rainfall": 0,
            "vehicle_count": 150,
            "speed": 40
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
