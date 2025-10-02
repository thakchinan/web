@echo off
echo ============================================
echo   Cloudflare Tunnel - Quick Start
echo ============================================
echo.
echo Starting Cloudflare Tunnel...
echo This will create a public URL for http://localhost:8000
echo.
echo NOTE: Make sure FastAPI server is running first!
echo       Run 'start_server.bat' in another terminal.
echo.

cloudflared tunnel --url http://localhost:8000

pause

