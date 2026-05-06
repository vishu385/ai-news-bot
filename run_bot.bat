@echo off
title AI News WhatsApp Bot
echo ============================================
echo    AI News WhatsApp Bot - Starting...
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b
)

REM Install dependencies if not already installed
echo Installing / verifying dependencies...
pip install -r "%~dp0requirements.txt" --quiet
echo.

REM Run the bot
echo Starting bot...
echo.
python "%~dp0ai_news_bot.py"

pause
