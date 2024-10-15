from .base import *

DEBUG = False

ALLOWED_HOSTS = ['capstone-task-managemt-7e87cf4b9f34.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

DATABASES['default']['CONN_MAX_AGE'] = 500

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
