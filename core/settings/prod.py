import os
from .base import *

# Ne pas activer le debug en prod !
DEBUG = False

# Définir ALLOWED_HOSTS via .env
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Paramètres de sécurité (HTTPS, Cookies)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
