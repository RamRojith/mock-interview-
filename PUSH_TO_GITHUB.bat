@echo off
echo ========================================
echo AI Mock Interview - GitHub Push Script
echo ========================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo After installation, restart this script.
    echo.
    pause
    exit /b 1
)

echo Git is installed. Proceeding...
echo.

REM Initialize repository if not already initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo.
)

REM Configure Git (update with your details)
echo Configuring Git...
git config user.name "RamRojith"
git config user.email "your.email@example.com"
echo.

REM Add all files
echo Adding all files...
git add .
echo.

REM Commit changes
echo Committing changes...
git commit -m "AI Mock Interview Portal - ERP Design System Implementation"
echo.

REM Add remote if not exists
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo Adding remote repository...
    git remote add origin https://github.com/RamRojith/mock-interview-.git
    echo.
)

REM Set main branch
echo Setting main branch...
git branch -M main
echo.

REM Push to GitHub
echo Pushing to GitHub...
echo.
echo NOTE: You may be asked for GitHub credentials.
echo Use your GitHub username and Personal Access Token (not password).
echo Generate token at: https://github.com/settings/tokens
echo.
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo SUCCESS! Code pushed to GitHub!
    echo ========================================
    echo.
    echo Repository: https://github.com/RamRojith/mock-interview-.git
    echo.
) else (
    echo.
    echo ========================================
    echo ERROR: Push failed!
    echo ========================================
    echo.
    echo Common issues:
    echo 1. Authentication failed - Use Personal Access Token
    echo 2. Repository doesn't exist - Create it on GitHub first
    echo 3. No internet connection
    echo.
)

pause
