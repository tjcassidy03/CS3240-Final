"""
WSGI config for ifcjcwhistleblower project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import dotenv
from django.core.wsgi import get_wsgi_application

dotenv.load_dotenv()

if os.getenv("ENV") == "Heroku":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ifcjcwhistleblower.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ifcjcwhistleblower.settings.local_settings')

application = get_wsgi_application()
