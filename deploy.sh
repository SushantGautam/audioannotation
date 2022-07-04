. venv/bin/activate
python manage.py collectstatic --noinput
systemctl restart gunicorn
systemctl restart nginx
systemctl restart celery-sound_annotation