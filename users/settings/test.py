import os
from .base import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'users.settings.test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3'),
    }
}
