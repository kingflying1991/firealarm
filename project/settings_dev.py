DEBUG = True
DEVELOPMENT, PRODUCTION = True, False
DEBUG_TOOLBAR = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fire_data_analysis',
        'USER': 'xiangw',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
CACHES = {
    'default': {
        'LOCATION': 'my_cache_table',
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        #'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    }
}
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
STATIC_URL = '/static/'
