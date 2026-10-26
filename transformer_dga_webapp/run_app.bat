@echo off
title Transformer DGA Intelligence Platform Launcher
echo ==============================================================================
echo     TRANSFORMER DGA INTELLIGENCE PLATFORM
echo     PRML-Based Power Transformer Fault Diagnosis Platform
echo     Developer: Mourya Abbadasari | Electrical Engineering, IIT Tirupati
echo ==============================================================================
echo.

cd /d "%~dp0"

set PYTHON_CMD=python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    set PYTHON_CMD="C:\Users\india\AppData\Local\Python\pythoncore-3.14-64\python.exe"
)

echo [1/3] Checking environment and dependencies...
echo Using Python: %PYTHON_CMD%

echo [2/3] Launching Streamlit web application on port 8501...
start "Transformer DGA Server" /B %PYTHON_CMD% -m streamlit run app.py --server.port 8501 --server.headless false

echo [3/3] Opening Google Chrome...
timeout /t 3 /nobreak >nul
start chrome "http://localhost:8501" 2>nul
if %ERRORLEVEL% NEQ 0 (
    start http://localhost:8501
)

echo.
echo ==============================================================================
echo Application is running at:
echo    Local URL:  http://localhost:8501
echo.
echo Press any key to exit this launcher window (server stays running in background).
echo ==============================================================================
pause >nul
