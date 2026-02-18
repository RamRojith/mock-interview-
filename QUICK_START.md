# Quick Start Guide - AI Mock Interview System

## 🚀 Starting the Application (Recommended Method)

### Windows Users:

**Double-click `start_services.bat`** or run in terminal:
```bash
cd mock_interview_system
start_services.bat
```

This will automatically:
1. ✅ Check if Ollama is installed
2. ✅ Start Ollama service
3. ✅ Download llama3 model (if needed)
4. ✅ Start Django server

### Manual Method (If Automated Script Fails):

**Terminal 1 - Start Ollama:**
```bash
ollama serve
```
Keep this terminal open!

**Terminal 2 - Start Django:**
```bash
cd mock_interview_system
python manage.py runserver
```

## 📋 First Time Setup

### 1. Install Ollama
Download and install from: https://ollama.ai

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download AI Model
```bash
ollama pull llama3
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

## 🎯 Using the Application

1. **Open Browser**: Navigate to `http://127.0.0.1:8000/`

2. **Test Microphone**: Click "Microphone Test" to ensure your mic works

3. **Start Interview**: 
   - Click "Start Interview"
   - Enter interview topic (e.g., "Python Developer")
   - Click "Login to Interview Portal"

4. **During Interview**:
   - Listen to the question
   - Click "Start Recording" to answer
   - Click "Stop Recording" when done
   - Wait for feedback and next question

5. **View Report**: After completing questions, view your comprehensive report

## ⚠️ Common Issues

### "Error when clicking Start Interview"

**Solution**: Make sure Ollama is running!
```bash
# Check if Ollama is running
ollama list

# If not, start it
ollama serve
```

### "Microphone not working"

**Solution**: 
1. Allow microphone access in browser
2. Check system microphone settings
3. Try the "Microphone Test" page

### "Slow response times"

**Solution**: 
- First time loading Whisper model takes time
- Subsequent requests will be faster
- Ensure stable internet connection

## 🔧 Service Status Check

Check if all services are running:
```bash
# Check Ollama
ollama list

# Check Django
python manage.py check

# Check health endpoint
# Open in browser: http://127.0.0.1:8000/api/health/
```

## 💡 Tips for Best Experience

1. **Always use `start_services.bat`** - It handles everything automatically
2. **Keep Ollama running** - Don't close the Ollama terminal
3. **Use Chrome or Edge** - Best browser compatibility
4. **Stable internet** - Required for text-to-speech
5. **Quiet environment** - For better speech recognition

## 🔄 Daily Startup Routine

Every time you want to use the application:

1. Run `start_services.bat`
2. Wait for "Starting development server" message
3. Open browser to `http://127.0.0.1:8000/`
4. Start interviewing!

## 📊 System Requirements

- **OS**: Windows 10/11
- **RAM**: 8GB minimum (16GB recommended)
- **Disk**: 10GB free space
- **Internet**: Stable connection
- **Browser**: Chrome, Edge, or Firefox

## 🆘 Need Help?

1. Check `TROUBLESHOOTING.md` for detailed solutions
2. Review console output for error messages
3. Ensure all dependencies are installed
4. Restart all services

## 🎓 Interview Tips

1. **Speak clearly** - Better transcription accuracy
2. **Take your time** - No rush to answer
3. **Be specific** - Detailed answers get better scores
4. **Practice regularly** - Improve with each session
5. **Review reports** - Learn from feedback

## 📝 Project Structure

```
mock_interview_system/
├── start_services.bat          # Automated startup script
├── manage.py                   # Django management
├── interview_core/             # Main application
│   ├── views.py               # API endpoints
│   ├── ai_service.py          # AI integration
│   └── templates/             # HTML pages
├── media/                      # Audio files
├── QUICK_START.md             # This file
└── TROUBLESHOOTING.md         # Detailed troubleshooting
```

## 🔐 Security Notes

- This is a development server
- Not suitable for production deployment
- Keep API keys secure
- Don't expose to public internet

## 📞 Support

For issues or questions:
1. Check error messages in console
2. Review `TROUBLESHOOTING.md`
3. Verify all services are running
4. Check system requirements

---

**Ready to start?** Run `start_services.bat` and begin your interview practice! 🎤
