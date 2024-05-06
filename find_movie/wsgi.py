"""
WSGI config for find_movie project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "find_movie.settings")

application = get_wsgi_application()
application = WhiteNoise(application)
