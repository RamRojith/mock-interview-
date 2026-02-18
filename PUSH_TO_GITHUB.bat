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
git config user.email "ramrojith@example.com"
echo.

REM Check if remote exists
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo Adding remote repository...
    git remote add origin https://github.com/RamRojith/mock-interview-.git
    echo Remote added successfully!
    echo.
) else (
    echo Remote already exists. Checking URL...
    git remote -v
    echo.
    echo If the URL is wrong, run: git remote set-url origin https://github.com/RamRojith/mock-interview-.git
    echo.
)

REM Add all files
echo Adding all files...
git add .
echo.

REM Check if there are changes to commit
git diff-index --quiet HEAD -- >nul 2>&1
if %errorlevel% neq 0 (
    echo Committing changes...
    git commit -m "AI Mock Interview Portal - Complete ERP Design with Report Generation"
    echo.
) else (
    echo No changes to commit. Checking if we need to push...
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
echo Username: Your GitHub username (RamRojith)
echo Password: Use your Personal Access Token (NOT your GitHub password)
echo.
echo Generate token at: https://github.com/settings/tokens
echo Select "repo" scope when creating the token
echo.
pause
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
    echo 1. Authentication failed - Use Personal Access Token as password
    echo 2. Repository doesn't exist - Create it on GitHub first
    echo 3. No internet connection
    echo 4. Remote URL is incorrect
    echo.
    echo To fix remote URL, run:
    echo git remote set-url origin https://github.com/RamRojith/mock-interview-.git
    echo.
)

pause
