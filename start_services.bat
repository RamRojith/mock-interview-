@echo off
echo ========================================
echo AI Mock Interview System - Service Starter
echo ========================================
echo.

REM Check if Ollama is installed
where ollama >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ollama is not installed or not in PATH
    echo Please install Ollama from: https://ollama.ai
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Ollama service...
ollama list >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Ollama service is not running. Starting Ollama...
    start "Ollama Service" ollama serve
    timeout /t 5 /nobreak >nul
    echo Ollama service started.
) else (
    echo Ollama service is already running.
)

echo.
echo [2/3] Checking if llama3 model is available...
ollama list | findstr "llama3" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo llama3 model not found. Pulling llama3 model...
    echo This may take a few minutes...
    ollama pull llama3
    echo llama3 model downloaded successfully.
) else (
    echo llama3 model is available.
)

echo.
echo [3/3] Starting Django development server...
echo.
python manage.py runserver

pause
