import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miettes.settings')

application = get_wsgi_application()

os.environ["HTTPS"] = "on"
os.environ["wsgi.url_scheme"] = "https"