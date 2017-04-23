"""
WSGI config for SecondHandsBook project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SecondHandsBook.settings")

application = get_wsgi_application()


"""
import os

import sys

reload(sys)
sys.setdefaultencoding('utf8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SecondHandsBook.settings")

from django.core.handlers.wsgi import WSGIHandler

application = WSGIHandler()
"""