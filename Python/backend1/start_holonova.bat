@echo off
title HoloNova - 3D Screenless Display System

cd /d "%~dp0"

echo.
echo ==========================================
echo             HoloNova
echo      3D Screenless Display System
echo ==========================================
echo.
echo Starting HoloNova...

start "" powershell -Command "Start-Sleep -Seconds 3; Start-Process 'http://127.0.0.1:8010/'"

python -m uvicorn main:app --host 127.0.0.1 --port 8010

pause