release: |
  echo "=== STARTING RELEASE PHASE ==="
  echo "Applying database migrations..."
  python manage.py migrate --no-input

  echo "Creating admin user if not exists..."
  python manage.py shell -c "
  import os
  from django.contrib.auth import get_user_model
  User = get_user_model()

  admin_email = os.environ.get('ADMIN_EMAIL')
  admin_password = os.environ.get('ADMIN_PASSWORD')

  if not User.objects.filter(email=admin_email).exists():
      User.objects.create_superuser(
          email=admin_email,
          password=admin_password
      )
      print(f'✅ Created superuser: {admin_email}')
  else:
      print(f'ℹ️ Admin {admin_email} already exists')
  "

  echo "Collecting static files..."
  python manage.py collectstatic --no-input

web: |
  echo "=== STARTING WEB SERVER ==="
  echo "Using PORT: $PORT"
  echo "Database: $DATABASE_URL"
  gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --access-logfile - \
    --error-logfile - \
    --timeout 120