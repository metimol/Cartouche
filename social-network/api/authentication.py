from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class StaticAPIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication using a static API key in the header 'X-API-KEY'.
    """
    def authenticate(self, request):
        # Allow unauthenticated access to API docs and schema
        path = request.path
        if path.startswith('/api/docs') or path.startswith('/api/schema'):
            return None
        # Allow unauthenticated access if Swagger UI sends 'Authorization' header (for the authorize button)
        if request.headers.get('Authorization'):
            return None
        api_key = request.headers.get('X-API-KEY')
        if not api_key or api_key != getattr(settings, 'STATIC_API_KEY', None):
            raise AuthenticationFailed('Invalid or missing API key.')
        return (None, None)  # No user, but authentication passed
