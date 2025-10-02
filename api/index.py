import os
import json
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Fix numpy._core issue for Python 3
import sys

# Force numpy to work with older versions
try:
    import numpy._core
except ImportError:
    try:
        import numpy.core as _core
        sys.modules['numpy._core'] = _core
    except ImportError:
        try:
            from numpy import _core
            sys.modules['numpy._core'] = _core
        except ImportError:
            try:
                from numpy.core import _core
                sys.modules['numpy._core'] = _core
            except ImportError:
                try:
                    from numpy.core._core import _core
                    sys.modules['numpy._core'] = _core
                except ImportError:
                    # If all else fails, create a dummy _core module
                    class DummyCore:
                        def __getattr__(self, name):
                            return lambda *args, **kwargs: None
                    sys.modules['numpy._core'] = DummyCore()

# ===== FastAPI setup =====
app = FastAPI(title="Traffic Congestion Predictor", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# Traffic Jam Model
jam_model = None
try:
    # Try to load model with error handling
    jam_model = joblib.load("models/rf_model.pkl")
    print("✅ โหลดโมเดล Traffic Jam (Random Forest) สำเร็จ")
except Exception as e:
    print(f"❌ ไม่สามารถโหลดโมเดล Traffic Jam: {e}")

# Day Type Model (ใช้โมเดลเดียวกันสำหรับตอนนี้)
day_model = None
try:
    day_model = joblib.load("models/rf_model.pkl")
    print("✅ โหลดโมเดล Day Type (Random Forest) สำเร็จ")
except Exception as e:
    print(f"❌ ไม่สามารถโหลดโมเดล Day Type: {e}")

# ===== Feature Engineering =====
def create_jam_features(data):
    """สร้างฟีเจอร์สำหรับการทำนายการจราจรติด/ไม่ติด"""
    features = []
    
    # Time-based features
    if 'hour' in data:
        features.append(data['hour'])
    else:
        features.append(12)  # Default to noon
    
    if 'day_of_week' in data:
        features.append(data['day_of_week'])
    else:
        features.append(1)  # Default to Monday
    
    # Weather features (if available)
    if 'temperature' in data:
        features.append(data['temperature'])
    else:
        features.append(25)  # Default temperature
    
    if 'humidity' in data:
        features.append(data['humidity'])
    else:
        features.append(60)  # Default humidity
    
    if 'rainfall' in data:
        features.append(data['rainfall'])
    else:
        features.append(0)  # Default no rain
    
    # Traffic volume features
    if 'vehicle_count' in data:
        features.append(data['vehicle_count'])
    else:
        features.append(100)  # Default vehicle count
    
    if 'speed' in data:
        features.append(data['speed'])
    else:
        features.append(50)  # Default speed
    
    return np.array(features).reshape(1, -1)

def create_day_features(data):
    """สร้างฟีเจอร์สำหรับการทำนายประเภทวัน"""
    features = []
    
    # Time-based features
    if 'hour' in data:
        features.append(data['hour'])
    else:
        features.append(12)
    
    if 'day_of_week' in data:
        features.append(data['day_of_week'])
    else:
        features.append(1)
    
    # Weather features
    if 'temperature' in data:
        features.append(data['temperature'])
    else:
        features.append(25)
    
    if 'humidity' in data:
        features.append(data['humidity'])
    else:
        features.append(60)
    
    if 'rainfall' in data:
        features.append(data['rainfall'])
    else:
        features.append(0)
    
    # Traffic volume features
    if 'vehicle_count' in data:
        features.append(data['vehicle_count'])
    else:
        features.append(100)
    
    if 'speed' in data:
        features.append(data['speed'])
    else:
        features.append(50)
    
    return np.array(features).reshape(1, -1)

# ===== API Endpoints =====
@app.get("/")
async def root():
    """หน้าแรกของแอปพลิเคชัน"""
    return {
        "message": "Traffic Congestion Predictor API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict_jam": "/predict/jam",
            "predict_day": "/predict/day",
            "predict_both": "/predict/both",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health():
    return {
        "status": "ok", 
        "jam_model": "loaded" if jam_model is not None else "not_loaded",
        "day_model": "loaded" if day_model is not None else "not_loaded"
    }

@app.post("/predict/jam")
async def predict_traffic_jam(data: dict):
    """ทำนายการจราจรติด/ไม่ติด"""
    try:
        if jam_model is None:
            return {"error": "โมเดลยังไม่พร้อมใช้งาน"}
        
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
            }
        }
        
        return result
        
    except Exception as e:
        return {"error": f"เกิดข้อผิดพลาด: {str(e)}"}

@app.post("/predict/day")
async def predict_day_type(data: dict):
    """ทำนายประเภทวัน (วันทำงาน/วันหยุด)"""
    try:
        if day_model is None:
            return {"error": "โมเดลยังไม่พร้อมใช้งาน"}
        
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
            }
        }
        
        return result
        
    except Exception as e:
        return {"error": f"เกิดข้อผิดพลาด: {str(e)}"}

@app.post("/predict/both")
async def predict_both(data: dict):
    """ทำนายทั้งการจราจรติดและประเภทวัน"""
    try:
        jam_result = await predict_traffic_jam(data)
        day_result = await predict_day_type(data)
        
        return {
            "traffic_jam": jam_result,
            "day_type": day_result
        }
        
    except Exception as e:
        return {"error": f"เกิดข้อผิดพลาด: {str(e)}"}

# ===== Vercel Handler =====
# This is the entry point for Vercel
handler = app