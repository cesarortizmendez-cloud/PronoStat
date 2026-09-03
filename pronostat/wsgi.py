"""WSGI para PronoStat. Vercel usa `app` como callable (@vercel/python)."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pronostat.settings')
application = get_wsgi_application()
app = application  # Vercel busca `app`
