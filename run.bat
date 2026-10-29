@echo off
title Virtual Steering Wheel - Industry 4.0
cd /d "%~dp0"

echo ========================================================
echo   Launching Virtual Steering Wheel Simulator...
echo ========================================================

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" virtual_steering_wheel.py
) else (
    python virtual_steering_wheel.py
)

pause
