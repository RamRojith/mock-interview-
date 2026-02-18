import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Set admin password
admin = User.objects.get(username='admin')
admin.set_password('admin123')
admin.save()

print("Admin password set successfully!")
print("Username: admin")
print("Password: admin123")
