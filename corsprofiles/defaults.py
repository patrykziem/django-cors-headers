from django.conf import settings

CORS_DEFAULT_ALLOW_HEADERS = getattr(settings, 'CORS_DEFAULT_ALLOW_HEADERS', (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
))

CORS_DEFAULT_ALLOW_METHODS = getattr(settings, 'CORS_DEFAULT_ALLOW_METHODS', (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
))

CORS_DEFAULT_PREFLIGHT_MAX_AGE = getattr(settings, 'CORS_DEFAULT_PREFLIGHT_MAX_AGE', 86400)

CORS_DEFAULT_EXPOSE_HEADERS = getattr(settings, 'CORS_DEFAULT_EXPOSE_HEADERS', ())

CORS_PROFILES = getattr(settings, 'CORS_PROFILES', [
    {
        'allow_all': True,
        'urls': r'^.+$',
    }
])
