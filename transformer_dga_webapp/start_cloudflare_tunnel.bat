@echo off
title Cloudflare Public Web Tunnel
cd /d "%~dp0"
echo ==============================================================================
echo   STARTING HIGH-SPEED CLOUDFLARE PUBLIC TUNNEL
echo   Connecting your local app to Cloudflare Edge Network...
echo ==============================================================================
echo.
cloudflared.exe tunnel --protocol http2 --url http://localhost:8501
pause
