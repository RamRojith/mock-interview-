# GitHub Push Instructions

## Quick Start (Automated)

1. **Install Git** (if not already installed):
   - Download: https://git-scm.com/download/win
   - Run installer with default settings
   - Restart your terminal

2. **Run the Push Script**:
   - Double-click `PUSH_TO_GITHUB.bat`
   - Follow the prompts
   - Enter your GitHub credentials when asked

## Manual Steps (Alternative)

### Step 1: Install Git
Download and install from: https://git-scm.com/download/win

### Step 2: Open Terminal in Project Folder
```bash
cd "C:\Users\Annamalai\Desktop\ram rojith - ai interview\mock_interview_system"
```

### Step 3: Configure Git (First Time Only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 4: Initialize and Push
```bash
# Initialize repository
git init

# Add all files
git add .

# Commit changes
git commit -m "AI Mock Interview Portal - ERP Design System"

# Add remote repository
git remote add origin https://github.com/RamRojith/mock-interview-.git

# Set main branch and push
git branch -M main
git push -u origin main
```

## GitHub Authentication

When prompted for credentials:
- **Username**: Your GitHub username (RamRojith)
- **Password**: Use a Personal Access Token (NOT your GitHub password)

### Generate Personal Access Token:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "Mock Interview Push"
4. Select scope: ✅ **repo** (full control of private repositories)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. Use this token as your password when pushing

## What Will Be Pushed

✅ **Templates**:
- Landing page with ERP design
- Interview start page
- Interview room interface
- Microphone test page
- Base template with header/footer

✅ **Styling**:
- Complete ERP design system (erp-style.css)
- Color reference guide
- Responsive layouts

✅ **JavaScript**:
- Interview room functionality
- Auto-help modal for microphone issues
- Audio recording and playback

✅ **Backend**:
- Django models and views
- AI service integration
- REST API endpoints
- Database migrations

✅ **Documentation**:
- UI Documentation
- Deployment Guide
- Page Flow Guide
- README with setup instructions

✅ **Configuration**:
- requirements.txt
- settings.py
- urls.py
- .gitignore

## Excluded Files (.gitignore)

❌ Python cache files (__pycache__)
❌ Database file (db.sqlite3)
❌ Media files (uploaded audio)
❌ IDE settings
❌ Environment variables

## Troubleshooting

### "Git is not recognized"
- Install Git from https://git-scm.com/download/win
- Restart your terminal after installation

### "Authentication failed"
- Use Personal Access Token, not your password
- Generate token at: https://github.com/settings/tokens
- Make sure token has "repo" scope

### "Repository not found"
- Make sure the repository exists on GitHub
- Check the URL: https://github.com/RamRojith/mock-interview-.git
- Verify you have access to the repository

### "Permission denied"
- Check if you're logged into the correct GitHub account
- Verify repository permissions
- Try using HTTPS instead of SSH

## After Successful Push

Your code will be available at:
```
https://github.com/RamRojith/mock-interview-
```

You can view it online and share with others!

## Future Updates

To push future changes:
```bash
git add .
git commit -m "Description of changes"
git push
```

---

**Need Help?**
- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com/
- Personal Access Tokens: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
