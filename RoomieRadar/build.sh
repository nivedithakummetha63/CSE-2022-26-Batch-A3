#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Create superuser automatically if not exists
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@roomieradar.com', 'Admin@1234')
    print("Superuser created: admin / Admin@1234")
else:
    print("Superuser already exists")
EOF
