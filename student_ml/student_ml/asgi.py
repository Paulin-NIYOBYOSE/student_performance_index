"""
ASGI config for student_ml project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_ml.settings")

application = get_asgi_application()
