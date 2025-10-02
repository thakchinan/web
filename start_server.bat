@echo off
echo ============================================
echo   Traffic Predictor - FastAPI Server
echo ============================================
echo.

cd /d "%~dp0"

echo [1/2] Starting FastAPI Server...
echo.

python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload

pause

