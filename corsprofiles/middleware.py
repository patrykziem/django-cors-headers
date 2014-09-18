import re
from django import http
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from corsprofiles import defaults as settings

ACCESS_CONTROL_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'
ACCESS_CONTROL_EXPOSE_HEADERS = 'Access-Control-Expose-Headers'
ACCESS_CONTROL_ALLOW_CREDENTIALS = 'Access-Control-Allow-Credentials'
ACCESS_CONTROL_ALLOW_HEADERS = 'Access-Control-Allow-Headers'
ACCESS_CONTROL_ALLOW_METHODS = 'Access-Control-Allow-Methods'
ACCESS_CONTROL_MAX_AGE = 'Access-Control-Max-Age'


class CorsMiddleware(object):

    def process_request(self, request):
        '''
            If CORS preflight header, then create an empty body response (200 OK) and return it

            Django won't bother calling any other request view/exception middleware along with
            the requested view; it will call any response middlewares
        '''
        if (self.is_enabled(request) and
            request.method == 'OPTIONS' and
            'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META):
            response = http.HttpResponse()
            return response
        return None

    def process_response(self, request, response):
        '''
            Add the respective CORS headers
        '''
        origin = request.META.get('HTTP_ORIGIN')

        if origin:
            url = urlparse(origin)
            for profile in settings.CORS_PROFILES:
                allow_all = profile.get('allow_all', True)
                allow_credentials = profile.get('allow_credentials', False)
                origin_whitelist = profile.get('origin_whitelist', ())
                expose_headers = profile.get(
                    'expose_headers', settings.CORS_DEFAULT_EXPOSE_HEADERS)
                allow_headers = profile.get(
                    'allow_headers', settings.CORS_DEFAULT_ALLOW_HEADERS)
                allow_methods = profile.get(
                    'allow_methods', settings.CORS_DEFAULT_ALLOW_METHODS)
                preflight_max_age = profile.get(
                    'preflight_max_age', settings.CORS_DEFAULT_PREFLIGHT_MAX_AGE)

                if self.request_matches_profile(request, profile):
                    if not allow_all and not url.netloc in origin_whitelist:
                        break

                    response[ACCESS_CONTROL_ALLOW_ORIGIN] = origin
                    if allow_all and not allow_credentials:
                        response[ACCESS_CONTROL_ALLOW_ORIGIN] = "*"

                    if len(expose_headers):
                        response[ACCESS_CONTROL_EXPOSE_HEADERS] = ', '.join(expose_headers)

                    if allow_credentials:
                        response[ACCESS_CONTROL_ALLOW_CREDENTIALS] = 'true'

                    if request.method == 'OPTIONS':
                        allow_headers = ', '.join(allow_headers)
                        response[ACCESS_CONTROL_ALLOW_HEADERS] = allow_headers
                        allow_methods = ', '.join(allow_methods)
                        response[ACCESS_CONTROL_ALLOW_METHODS] = allow_methods
                        if preflight_max_age:
                            response[ACCESS_CONTROL_MAX_AGE] = preflight_max_age

                    break

        return response

    def request_matches_profile(self, request, profile):
        if isinstance(profile['urls'], tuple):
            for url in profile['urls']:
                if re.match(url, request.path):
                    return True
            return False
        else:
            return re.match(profile['urls'], request.path)

    def is_enabled(self, request):
        for profile in settings.CORS_PROFILES:
            if self.request_matches_profile(request, profile):
                return True

        return False
