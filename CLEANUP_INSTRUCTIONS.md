# Cleanup Instructions

## Manual Cleanup Required

The project structure has been updated to use a `config` folder instead of the nested `mock_interview_system` folder for better clarity.

### Old Structure (Confusing):
```
mock_interview_system/
├── mock_interview_system/    ← Settings folder (same name as root)
│   ├── settings.py
│   └── ...
```

### New Structure (Clear):
```
mock_interview_system/
├── config/                   ← Settings folder (clear name)
│   ├── settings.py
│   └── ...
```

## Action Required

**Please manually delete the old `mock_interview_system/mock_interview_system/` folder:**

1. Close VS Code completely
2. Stop any running Python/Django processes
3. Navigate to the project folder
4. Delete the `mock_interview_system/mock_interview_system/` folder
5. Reopen VS Code

The folder is currently locked by a running process, so it cannot be deleted automatically.

## Verification

After cleanup, your project structure should look like:

```
mock_interview_system/
├── config/                   ← Django settings (NEW)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── interview_core/           ← Django app
├── media/                    ← Media files
├── static/                   ← Static files
├── manage.py
├── requirements.txt
└── start_services.bat
```

## Files Updated

The following files have been updated to reference `config` instead of `mock_interview_system`:

- ✅ `manage.py` - Updated DJANGO_SETTINGS_MODULE
- ✅ `config/settings.py` - Updated ROOT_URLCONF
- ✅ `config/wsgi.py` - Updated settings module
- ✅ `config/asgi.py` - Updated settings module

## Testing

After cleanup, test the application:

```bash
# Check for errors
python manage.py check

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Everything should work exactly as before, just with a clearer folder structure!
