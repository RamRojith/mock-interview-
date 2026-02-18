# AI Mock Interview Portal - ERP-Styled UI Documentation

## Overview
The AI Mock Interview module has been redesigned to match the Ramco Institute of Technology (RIT) ERP portal design system, providing a seamless, professional, and institutional experience.

## Design System

### Color Palette
- **Primary Blue**: `#2F4C9F` - Main brand color
- **Secondary Blue**: `#3B5FCC` - Accent and hover states
- **Background**: `#F8FAFC` - Page background
- **Card White**: `#FFFFFF` - Card backgrounds
- **Text Dark**: `#1F2937` - Primary text
- **Text Gray**: `#6B7280` - Secondary text
- **Success Green**: `#10B981` - Success actions
- **Danger Red**: `#EF4444` - Danger actions

### Typography
- **Font Family**: Segoe UI, -apple-system, BlinkMacSystemFont, Roboto, Oxygen, Ubuntu
- **Academic & Professional**: Clean, readable, institutional

## Page Structure

### 1. Landing Page (`/`)
**Route**: `/`
**Template**: `landing.html`
**Purpose**: Main entry point showcasing AI Interview services

**Features**:
- ERP-style header with RIT branding
- Hero section with welcome message
- Three portal cards:
  - Student Mock Interview (Active)
  - Interview History (Coming Soon)
  - Interview Guidelines (Coming Soon)

### 2. Interview Start Page (`/start/`)
**Route**: `/start/`
**Template**: `index.html`
**Purpose**: Student login and interview topic selection

**Features**:
- Centered form card
- Topic input field
- Microphone access notification
- Professional form validation

### 3. Interview Room (`/interview/<session_id>/`)
**Route**: `/interview/<session_id>/`
**Template**: `interview.html`
**Purpose**: Active interview session interface

**Features**:
- Question display in soft-grey box
- Audio player for AI questions
- Recording controls (Start/Stop)
- Status indicators:
  - Ready (default)
  - AI is listening... (recording)
  - AI is evaluating... (processing)
- Feedback card with score display

## Component Breakdown

### ERP Header
```html
- RIT Logo placeholder
- Institution name: "Ramco Institute of Technology"
- Subtitle: "Enterprise Resource Planning System"
- Gradient blue background
- Rounded bottom corners
```

### Portal Cards
```html
- Icon with gradient background
- Card title
- Description text
- Action button with arrow
- Hover elevation effect
- Consistent spacing and shadows
```

### Form Elements
```html
- Clean input fields with focus states
- Info boxes for important notices
- Primary action buttons
- Form hints and labels
```

### Interview Interface
```html
- Question display box
- Audio player integration
- Control buttons (Success/Danger colors)
- Status badges with color coding
- Feedback card with score display
```

## Responsive Design

### Desktop (>768px)
- Full-width header
- Multi-column card grid
- Spacious padding and margins

### Mobile (<768px)
- Stacked header elements
- Single-column card layout
- Full-width buttons
- Optimized touch targets

## File Structure

```
mock_interview_system/
├── interview_core/
│   ├── templates/
│   │   └── interview_core/
│   │       ├── base.html          # Base template with header/footer
│   │       ├── landing.html       # Landing page
│   │       ├── index.html         # Interview start form
│   │       └── interview.html     # Interview room
│   ├── views.py                   # View functions
│   └── urls.py                    # URL routing
├── static/
│   ├── css/
│   │   └── erp-style.css         # Complete ERP design system
│   └── js/
│       └── interview.js          # Interview room functionality
└── UI_DOCUMENTATION.md           # This file
```

## Key Features

### Professional Design
- No emojis or casual elements
- Academic language throughout
- Institutional color scheme
- Clean, minimal animations

### Accessibility
- Proper semantic HTML
- ARIA-friendly structure
- Keyboard navigation support
- Clear focus states

### User Experience
- Clear status indicators
- Informative feedback
- Smooth transitions
- Error handling

## Integration Notes

### Static Files
- CSS is loaded via `{% static 'css/erp-style.css' %}`
- JS is loaded via `{% static 'js/interview.js' %}`
- Ensure `python manage.py collectstatic` is run for production

### Media Files
- Audio files stored in `media/tts/`
- Response recordings in `media/responses/`
- Served via Django's media URL in development

### CSRF Protection
- All forms include CSRF tokens
- AJAX requests include CSRF headers
- Cookie-based token retrieval

## Future Enhancements

### Planned Features
1. **Interview History Page**
   - View past interview sessions
   - Score trends and analytics
   - Detailed feedback review

2. **Interview Guidelines Page**
   - How the AI interview works
   - Preparation tips
   - Technical requirements

3. **User Authentication**
   - Student login with register number
   - College email verification
   - Session management

4. **Advanced Features**
   - Department-specific questions
   - Difficulty level selection
   - Interview report generation
   - Performance analytics dashboard

## Browser Support
- Chrome/Edge (Recommended)
- Firefox
- Safari
- Opera

**Note**: Microphone access required for interview functionality.

## Maintenance

### Updating Colors
Edit CSS variables in `erp-style.css`:
```css
:root {
    --primary-blue: #2F4C9F;
    --secondary-blue: #3B5FCC;
    /* ... */
}
```

### Adding New Pages
1. Create template extending `base.html`
2. Add view function in `views.py`
3. Register route in `urls.py`
4. Use existing CSS classes for consistency

### Customizing Components
All components use modular CSS classes:
- `.portal-card` - Service cards
- `.form-card` - Form containers
- `.interview-card` - Interview interface
- `.btn-primary`, `.btn-success`, `.btn-danger` - Buttons

---

**Developed for**: Ramco Institute of Technology  
**Module**: AI Mock Interview Portal  
**Design System**: RIT ERP Institutional Style  
**Version**: 1.0  
**Last Updated**: February 2026
