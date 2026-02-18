# Troubleshooting Guide - AI Mock Interview System

## Common Issues and Solutions

### 1. Error When Clicking "Start Interview"

#### Symptoms:
- Error message appears when clicking "Start Interview" button
- Interview doesn't start
- Error persists after closing and reopening the application

#### Root Causes:
1. **Ollama service not running**
2. **llama3 model not downloaded**
3. **Whisper model loading issues**
4. **Edge-TTS connectivity problems**

#### Solutions:

##### Option 1: Use the Automated Startup Script (Recommended)
```bash
# Navigate to project directory
cd mock_interview_system

# Run the startup script
start_services.bat
```

This script will:
- Check if Ollama is installed
- Start Ollama service if not running
- Download llama3 model if missing
- Start Django server

##### Option 2: Manual Setup

**Step 1: Check Ollama Installation**
```bash
ollama --version
```
If not installed, download from: https://ollama.ai

**Step 2: Start Ollama Service**
```bash
# Start Ollama in a separate terminal
ollama serve
```

**Step 3: Pull llama3 Model**
```bash
# In another terminal
ollama pull llama3
```

**Step 4: Verify Ollama is Working**
```bash
ollama list
```
You should see llama3 in the list.

**Step 5: Start Django Server**
```bash
python manage.py runserver
```

### 2. Microphone Not Working

#### Solutions:
1. Test microphone using the "Microphone Test" button on landing page
2. Check browser permissions (allow microphone access)
3. Ensure microphone is not being used by another application
4. Try a different browser (Chrome recommended)

### 3. Audio Playback Issues

#### Solutions:
1. Check system volume
2. Ensure speakers/headphones are connected
3. Check browser audio permissions
4. Clear browser cache

### 4. Slow Response Times

#### Causes:
- First-time model loading (Whisper)
- Ollama processing time
- Network issues (Edge-TTS)

#### Solutions:
1. Wait for initial model loading (happens once)
2. Ensure stable internet connection
3. Close unnecessary applications

### 5. Database Errors

#### Solutions:
```bash
# Reset database
python manage.py migrate --run-syncdb

# Create new migrations if needed
python manage.py makemigrations
python manage.py migrate
```

## System Requirements

### Minimum Requirements:
- Python 3.8+
- 8GB RAM (16GB recommended)
- 10GB free disk space
- Stable internet connection
- Modern web browser (Chrome, Firefox, Edge)

### Required Services:
1. **Ollama** - AI model inference
2. **Whisper** - Speech-to-text
3. **Edge-TTS** - Text-to-speech

## Service Status Check

### Check if all services are running:

```bash
# Check Ollama
ollama list

# Check Python packages
pip list | findstr "whisper"
pip list | findstr "edge-tts"
pip list | findstr "ollama"

# Check Django
python manage.py check
```

## Fallback Mode

The system now includes **automatic fallback mode**:
- If Ollama is unavailable, the system uses pre-defined questions
- If Whisper fails, error messages are shown
- If Edge-TTS fails, questions are displayed as text

This ensures the interview can continue even if some services are down.

## Getting Help

If issues persist:
1. Check the console output for error messages
2. Review Django logs
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Restart all services

## Quick Start Checklist

Before starting an interview:
- [ ] Ollama service is running
- [ ] llama3 model is downloaded
- [ ] Django server is running
- [ ] Microphone is working
- [ ] Internet connection is stable

## Automated Daily Startup

To avoid errors when opening the application on a new day:

1. **Always use `start_services.bat`** instead of running Django directly
2. Or create a desktop shortcut to `start_services.bat`
3. The script will automatically check and start all required services

## Performance Tips

1. Keep Ollama running in the background
2. Don't close the Ollama terminal window
3. Use a wired internet connection for better stability
4. Close unnecessary browser tabs
5. Restart services if they've been running for multiple days

## Error Messages Reference

| Error Message | Cause | Solution |
|--------------|-------|----------|
| "Ollama service not available" | Ollama not running | Run `ollama serve` |
| "Whisper model not loaded" | Model loading failed | Restart Django server |
| "Edge-TTS error" | No internet connection | Check network |
| "Failed to start session" | Database/API error | Check Django logs |
| "Audio file required" | Microphone not working | Test microphone |

## Contact & Support

For additional help, check:
- Django logs in the console
- Browser console (F12) for JavaScript errors
- System event logs for service issues
