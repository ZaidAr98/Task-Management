from split_settings.tools import include
from decouple import config

DJANGO_ENV = config('DJANGO_ENV', default='dev')

include('base.py')

if DJANGO_ENV == 'dev':
    include('development.py')
elif DJANGO_ENV == 'prod':
    include('production.py')
else:
    raise ValueError(f"Unknown DJANGO_ENV: {DJANGO_ENV}")
