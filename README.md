# AI Mock Interview System - RIT ERP Portal

A professional Django-based mock interview application styled to match the Ramco Institute of Technology (RIT) Enterprise Resource Planning (ERP) portal design system.

## 🎯 Features

### AI-Powered Interview System
- **Whisper** for Speech-to-Text transcription
- **Ollama (Llama-3)** for intelligent interview logic and feedback
- **Edge TTS** for natural voice output
- Real-time audio recording and processing
- Intelligent question generation based on responses
- Detailed AI feedback and scoring

### Professional ERP-Styled UI
- **Institutional Design**: Matches RIT ERP portal aesthetics
- **Responsive Layout**: Desktop-first, mobile-friendly
- **Clean Interface**: Professional academic styling
- **Accessible**: WCAG-friendly design patterns
- **Three Main Pages**:
  - Landing page with service cards
  - Interview start/login page
  - Interactive interview room

## 🎨 Design System

### Color Palette
- Primary Blue: `#2F4C9F`
- Secondary Blue: `#3B5FCC`
- Background: `#F8FAFC`
- Success Green: `#10B981`
- Danger Red: `#EF4444`

### Key Design Elements
- Gradient blue header with rounded corners
- Card-based portal selection
- Soft shadows and hover effects
- Status badges with color coding
- Professional typography (Segoe UI)

## 📋 Prerequisites

1. **Python 3.10+** (Installed)
2. **FFmpeg**: Required for audio processing
   - **Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extract, and add `bin` folder to System PATH
   - *Note: The app will fail to transcribe audio without this*
3. **Ollama**: Required for AI logic
   - Download from [ollama.com](https://ollama.com)
   - Run: `ollama pull llama3` (or `mistral`)

## 🚀 Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Dependencies are already installed in this environment)*

2. **Database Migration** (Already done):
   ```bash
   python manage.py migrate
   ```

3. **Collect Static Files** (for production):
   ```bash
   python manage.py collectstatic
   ```

## 🎮 Running the Application

1. Start the server:
   ```bash
   cd mock_interview_system
   python manage.py runserver
   ```

2. Access the application:
   - **Landing Page**: http://127.0.0.1:8000/
   - **Start Interview**: http://127.0.0.1:8000/start/
   - **Interview Room**: Automatically redirected after starting session

3. Using the Interview System:
   - Click "Start Interview →" on the landing page
   - Enter interview topic (e.g., "Python Developer", "Data Analyst")
   - Click "Login to Interview Portal"
   - Allow microphone access when prompted
   - Answer AI questions by clicking "Start Answer"
   - Receive instant feedback and scores

## 📁 Project Structure

```
mock_interview_system/
├── interview_core/
│   ├── templates/
│   │   └── interview_core/
│   │       ├── base.html          # Base template with ERP header
│   │       ├── landing.html       # Landing page with portal cards
│   │       ├── index.html         # Interview start form
│   │       └── interview.html     # Interview room interface
│   ├── models.py                  # Database models
│   ├── views.py                   # View functions
│   ├── urls.py                    # URL routing
│   ├── ai_service.py              # AI integration (Whisper, Ollama, TTS)
│   └── serializers.py             # REST API serializers
├── static/
│   ├── css/
│   │   ├── erp-style.css         # Complete ERP design system
│   │   └── color-reference.css   # Color palette reference
│   └── js/
│       └── interview.js          # Interview room functionality
├── media/
│   ├── tts/                      # Generated question audio
│   └── responses/                # User response recordings
├── UI_DOCUMENTATION.md           # Complete UI/UX documentation
├── DEPLOYMENT_GUIDE.md           # Deployment instructions
└── README.md                     # This file
```

## 🎯 Page Routes

| Route | Template | Purpose |
|-------|----------|---------|
| `/` | `landing.html` | Main landing page with service cards |
| `/start/` | `index.html` | Interview topic selection |
| `/interview/<id>/` | `interview.html` | Active interview session |
| `/api/start-session/` | API | Create new interview session |
| `/api/process-response/` | API | Process audio and generate feedback |

## 🛠️ Troubleshooting

### Audio Issues
- **"Error transcribing"**: Ensure FFmpeg is installed and in your PATH. Restart terminal after installing.
- **"Microphone access denied"**: Check browser permissions (Chrome/Edge recommended)
- **Audio not playing**: Verify media files exist in `media/tts/` directory

### AI Issues
- **"Unable to generate feedback"**: Ensure Ollama is running (`ollama serve`) and you have pulled the model (`ollama pull llama3`)
- **Slow responses**: AI processing takes time; wait for "AI is evaluating..." status

### UI Issues
- **CSS not loading**: Clear browser cache (Ctrl+Shift+R) and verify static files
- **Layout broken**: Check browser console for errors
- **Mobile view issues**: Test in responsive mode (F12 → Device toolbar)

## 📚 Documentation

- **UI_DOCUMENTATION.md**: Complete design system reference
- **DEPLOYMENT_GUIDE.md**: Production deployment guide
- **color-reference.css**: Color palette and usage guidelines

## 🌟 Key Features

### Landing Page
- Professional ERP-styled header
- Hero section with welcome message
- Three service cards:
  - Student Mock Interview (Active)
  - Interview History (Coming Soon)
  - Interview Guidelines (Coming Soon)

### Interview Start Page
- Clean form design
- Topic input with validation
- Microphone access notification
- Professional button styling

### Interview Room
- Real-time question display
- Audio playback for AI questions
- Recording controls with status indicators
- Instant AI feedback with scores
- Smooth transitions and animations

## 🔒 Security Notes

- CSRF protection enabled on all forms
- Secure cookie handling
- Input validation and sanitization
- Media file access controls

## 🚀 Future Enhancements

- User authentication (student login)
- Interview history and analytics
- Department-specific question banks
- Performance tracking dashboard
- Email notifications
- Multi-language support
- Video interview option

## 📝 License

This project is developed for Ramco Institute of Technology.

## 👥 Support

For issues or questions, refer to:
- UI_DOCUMENTATION.md for design questions
- DEPLOYMENT_GUIDE.md for setup issues
- Django documentation: https://docs.djangoproject.com/

---

**Developed for**: Ramco Institute of Technology  
**Module**: AI Mock Interview Portal  
**Design System**: RIT ERP Institutional Style  
**Version**: 1.0  
**Last Updated**: February 2026
