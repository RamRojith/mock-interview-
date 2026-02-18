# AI Mock Interview System

A comprehensive AI-powered mock interview platform with speech recognition, real-time feedback, and detailed performance reports.

## 🚀 Quick Start

### Start the Application (Easiest Way)
```bash
# Just double-click or run:
start_services.bat
```

This automatically handles everything:
- Checks Ollama installation
- Starts required services
- Downloads AI models
- Launches the application

### Access the Application
Open your browser to: **http://127.0.0.1:8000/**

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Step-by-step startup guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solutions to common issues
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Production deployment
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** - Git repository setup

## ✨ Features

### 🎤 Voice-Based Interviews
- Real-time speech-to-text using Whisper AI
- Natural text-to-speech responses
- Microphone testing and troubleshooting

### 🤖 AI-Powered Evaluation
- Intelligent question generation using Llama3
- Real-time feedback on answers
- Scoring based on relevance, clarity, and confidence

### 📊 Comprehensive Reports
- Interview performance analysis
- Grammar and language skills evaluation
- Detailed improvement suggestions
- Overall readiness assessment

### 🎨 Professional UI
- Modern ERP-style design
- Responsive layout
- Intuitive navigation
- Real-time status indicators

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **AI Models**: 
  - Whisper (Speech-to-Text)
  - Llama3 via Ollama (Interview AI)
  - Edge-TTS (Text-to-Speech)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite

## 📋 System Requirements

- **OS**: Windows 10/11
- **Python**: 3.8+
- **RAM**: 8GB minimum (16GB recommended)
- **Disk Space**: 10GB free
- **Internet**: Stable connection required
- **Browser**: Chrome, Edge, or Firefox

## 🔧 Installation

### 1. Install Ollama
Download from: https://ollama.ai

### 2. Clone Repository
```bash
git clone https://github.com/RamRojith/mock-interview-.git
cd mock_interview_system
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
python manage.py migrate
```

### 5. Download AI Model
```bash
ollama pull llama3
```

### 6. Start Application
```bash
start_services.bat
```

## 🎯 Usage Guide

### Starting an Interview

1. **Navigate to Home**: Open http://127.0.0.1:8000/
2. **Test Microphone**: Click "Microphone Test" (recommended)
3. **Start Interview**: Click "Start Interview"
4. **Enter Topic**: Specify role (e.g., "Python Developer")
5. **Begin Session**: Click "Login to Interview Portal"

### During the Interview

1. **Listen**: AI asks a question (audio + text)
2. **Record**: Click "Start Recording" to answer
3. **Stop**: Click "Stop Recording" when finished
4. **Feedback**: Receive score and feedback
5. **Continue**: Answer next question
6. **Complete**: Finish all questions

### Viewing Reports

1. Click "End Interview" or complete all questions
2. View comprehensive evaluation report
3. Review strengths and weaknesses
4. Get improvement suggestions
5. Download or print report

## 🔍 Service Health Check

Check if all services are running:
```bash
# Visit in browser:
http://127.0.0.1:8000/api/health/
```

Returns:
```json
{
  "status": "healthy",
  "services": {
    "ollama": true,
    "whisper": true,
    "edge_tts": true
  },
  "message": "All services operational"
}
```

## ⚠️ Troubleshooting

### Error: "Failed to start session"

**Cause**: Ollama service not running

**Solution**:
```bash
# Start Ollama in a separate terminal
ollama serve
```

### Error: "Microphone not working"

**Solution**:
1. Allow microphone access in browser
2. Check system microphone settings
3. Use "Microphone Test" page
4. Try different browser

### Error: "Slow response times"

**Solution**:
- First load takes time (model loading)
- Subsequent requests are faster
- Ensure stable internet connection
- Close unnecessary applications

For more solutions, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## 🔄 Fallback Mode

The system includes automatic fallback mode:
- **Ollama unavailable**: Uses pre-defined questions
- **Whisper fails**: Shows error messages
- **Edge-TTS fails**: Displays text-only questions

This ensures interviews can continue even if some services are down.

## 📁 Project Structure

```
mock_interview_system/
├── interview_core/              # Main Django app
│   ├── ai_service.py           # AI integration
│   ├── views.py                # API endpoints
│   ├── models.py               # Database models
│   ├── templates/              # HTML templates
│   └── migrations/             # Database migrations
├── mock_interview_system/       # Django project settings
├── media/                       # Audio files
│   ├── responses/              # User recordings
│   └── tts/                    # Generated speech
├── static/                      # CSS, JS, images
├── start_services.bat          # Automated startup
├── manage.py                   # Django management
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── QUICK_START.md             # Quick start guide
└── TROUBLESHOOTING.md         # Troubleshooting guide
```

## 🔐 Security Notes

- Development server only (not for production)
- Keep API keys secure
- Don't expose to public internet
- Use environment variables for sensitive data

## 🚀 Deployment

For production deployment, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 📝 API Endpoints

- `GET /` - Landing page
- `GET /start/` - Interview start page
- `GET /interview/<id>/` - Interview session
- `GET /report/<id>/` - Interview report
- `POST /api/start-session/` - Create interview session
- `POST /api/process-response/` - Process user response
- `GET /api/health/` - Service health check

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is for educational purposes.

## 👥 Authors

- Ram Rojith

## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition
- Ollama for AI model hosting
- Edge-TTS for text-to-speech
- Django community

## 📞 Support

For issues or questions:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review console error messages
3. Verify all services are running
4. Check system requirements

## 🎓 Tips for Best Results

1. **Environment**: Use in quiet space
2. **Microphone**: Use quality microphone
3. **Internet**: Ensure stable connection
4. **Browser**: Use Chrome for best compatibility
5. **Practice**: Regular practice improves scores

---

**Ready to practice?** Run `start_services.bat` and start your interview! 🎤✨
