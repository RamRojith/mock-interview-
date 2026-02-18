# AI Mock Interview Portal - Page Flow Guide

## User Journey

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  LANDING PAGE (/)                                           │
│  ═══════════════════════════════════════════════════════   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  RIT ERP HEADER                                     │   │
│  │  [RIT Logo] Ramco Institute of Technology          │   │
│  │             Enterprise Resource Planning System     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  HERO SECTION                                       │   │
│  │  Welcome to AI Mock Interview Portal               │   │
│  │  Practice technical and HR interviews using AI     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ Student  │  │Interview │  │Interview │                 │
│  │  Mock    │  │ History  │  │Guidelines│                 │
│  │Interview │  │          │  │          │                 │
│  │          │  │ (Coming) │  │ (Coming) │                 │
│  │ [Start →]│  │          │  │          │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Click "Start Interview →"
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  INTERVIEW START PAGE (/start/)                             │
│  ═══════════════════════════════════════════════════════   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  RIT ERP HEADER                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Student Login – AI Mock Interview                 │   │
│  │  Enter your details to begin the interview session │   │
│  │                                                     │   │
│  │  Interview Topic:                                  │   │
│  │  [_____________________________________]           │   │
│  │  e.g., Python Developer, Data Analyst              │   │
│  │                                                     │   │
│  │  ℹ️ Microphone access will be requested           │   │
│  │                                                     │   │
│  │  [Login to Interview Portal →]                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Submit Form
                            │ API: POST /api/start-session/
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  INTERVIEW ROOM (/interview/<session_id>/)                  │
│  ═══════════════════════════════════════════════════════   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  RIT ERP HEADER                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Mock Interview: Python Developer    [Ready]       │   │
│  │  ─────────────────────────────────────────────────  │   │
│  │                                                     │   │
│  │  CURRENT QUESTION                                  │   │
│  │  ┌───────────────────────────────────────────────┐ │   │
│  │  │ Tell me about yourself and your background.   │ │   │
│  │  └───────────────────────────────────────────────┘ │   │
│  │                                                     │   │
│  │  [🔊 Audio Player ═══════════════════════]         │   │
│  │                                                     │   │
│  │  [🎤 Start Answer]  [⏹ Stop & Submit]              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  AI EVALUATION                                      │   │
│  │  Score: 8/10                                        │   │
│  │                                                     │   │
│  │  Great answer! You clearly explained your          │   │
│  │  background and relevant experience...              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Flow

### 1. Landing Page (`/`)

**Purpose**: Welcome users and showcase available services

**Elements**:
- ERP-styled header with RIT branding
- Hero section with welcome message
- Three service cards (portal-style)
- Footer with copyright

**User Actions**:
- Click "Start Interview →" → Navigate to `/start/`
- View other service cards (placeholders)

**Design Notes**:
- Gradient blue header matching ERP
- Rounded hero section
- Card hover effects
- Responsive grid layout

---

### 2. Interview Start Page (`/start/`)

**Purpose**: Collect interview topic and initialize session

**Elements**:
- ERP header (consistent)
- Centered form card
- Topic input field
- Microphone access notification
- Submit button

**User Actions**:
1. Enter interview topic (e.g., "Python Developer")
2. Click "Login to Interview Portal"
3. System creates session via API
4. Redirect to interview room

**API Call**:
```javascript
POST /api/start-session/
Body: { "topic": "Python Developer" }
Response: { "session_id": 123, "first_question": "...", "audio_url": "..." }
```

**Design Notes**:
- Professional form styling
- Input validation
- Info box for important notices
- Loading state on button

---

### 3. Interview Room (`/interview/<session_id>/`)

**Purpose**: Conduct the actual interview with AI

**Elements**:
- ERP header (consistent)
- Interview card with:
  - Session title and status badge
  - Question display box
  - Audio player for AI questions
  - Recording controls
- Feedback card (appears after response)

**User Actions**:
1. **Listen** to AI question (auto-plays)
2. **Click** "Start Answer" → Microphone starts recording
3. **Speak** your answer
4. **Click** "Stop & Submit" → Audio sent to backend
5. **View** AI feedback and score
6. **Repeat** for next question

**Status Flow**:
```
Ready → AI is listening... → AI is evaluating... → Ready
```

**API Call**:
```javascript
POST /api/process-response/
Body: FormData {
  audio_file: Blob,
  session_id: 123
}
Response: {
  feedback: "Great answer!...",
  score: 8,
  next_question: { id: 456, text: "..." },
  audio_url: "/media/tts/question_456.mp3"
}
```

**Design Notes**:
- Status badges with color coding
- Smooth transitions
- Feedback card animation
- Professional button states

---

## State Management

### Status Badge States

| State | Color | When |
|-------|-------|------|
| Ready | Grey | Initial state, ready for input |
| AI is listening... | Blue | Recording in progress |
| AI is evaluating... | Yellow | Processing response |
| Error | Red | Error occurred |

### Button States

| Button | Enabled When | Disabled When |
|--------|-------------|---------------|
| Start Answer | Not recording | Recording active |
| Stop & Submit | Recording active | Not recording |

### Feedback Card

- **Hidden**: Initially and while recording
- **Visible**: After receiving AI response
- **Animation**: Fade in from bottom

---

## Responsive Behavior

### Desktop (>768px)
- Full-width header
- Three-column card grid
- Side-by-side buttons
- Spacious padding

### Mobile (<768px)
- Stacked header elements
- Single-column cards
- Full-width buttons
- Reduced padding

---

## Error Handling

### Microphone Access Denied
```
Status: "Error: Microphone access denied"
Action: Disable recording buttons
Message: Show browser permission instructions
```

### Network Error
```
Status: "Error sending response"
Action: Re-enable buttons
Message: "Please check your connection"
```

### Session Not Found
```
Action: Redirect to start page
Message: "Session expired, please start again"
```

---

## Audio Flow

### Question Audio (TTS)
1. Backend generates audio using Edge TTS
2. Saves to `media/tts/question_<id>.mp3`
3. Returns URL in API response
4. Frontend plays audio automatically

### Response Audio (Recording)
1. User clicks "Start Answer"
2. Browser MediaRecorder captures audio
3. User clicks "Stop & Submit"
4. Audio sent as Blob to backend
5. Backend saves to `media/responses/`
6. Whisper transcribes audio
7. Ollama generates feedback

---

## Navigation Flow

```
Landing (/) 
    ↓
Start (/start/)
    ↓
Interview (/interview/<id>/)
    ↓
[Future: Results (/results/<id>/)]
```

---

## Key Design Principles

1. **Consistency**: ERP header on every page
2. **Clarity**: Clear status indicators
3. **Feedback**: Immediate visual feedback for actions
4. **Accessibility**: Keyboard navigation, ARIA labels
5. **Professional**: No emojis, academic language
6. **Responsive**: Works on all devices

---

## Future Enhancements

### Interview History Page
```
/history/
- List of past interviews
- Scores and dates
- View detailed feedback
- Performance trends
```

### Guidelines Page
```
/guidelines/
- How AI interview works
- Preparation tips
- Technical requirements
- FAQ section
```

### User Authentication
```
/login/
- Register number input
- College email verification
- Password authentication
- Session management
```

---

**Last Updated**: February 2026  
**Version**: 1.0
