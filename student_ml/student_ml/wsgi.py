"""
WSGI config for student_ml project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_ml.settings")

application = get_wsgi_application()
