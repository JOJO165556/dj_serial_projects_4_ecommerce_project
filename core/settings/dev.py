from .base import *

# Ne pas activer le debug en prod !
DEBUG = True

ALLOWED_HOSTS = ['*']

# Désactiver la validation des mots de passe en dev
AUTH_PASSWORD_VALIDATORS = []
