# Project Structure - AI Mock Interview System

## Clean Directory Structure

```
mock_interview_system/                    # Root project directory
│
├── .git/                                 # Git version control
├── .gitignore                           # Git ignore rules
│
├── manage.py                            # Django management script
├── db.sqlite3                           # SQLite database
├── requirements.txt                     # Python dependencies
├── start_services.bat                   # Automated startup script
│
├── mock_interview_system/               # Django project settings (DO NOT add files here)
│   ├── __init__.py                     # Python package marker
│   ├── settings.py                     # Django settings
│   ├── urls.py                         # Main URL configuration
│   ├── wsgi.py                         # WSGI configuration
│   ├── asgi.py                         # ASGI configuration
│   └── __pycache__/                    # Python cache (auto-generated)
│
├── interview_core/                      # Main Django app
│   ├── __init__.py                     # Python pack