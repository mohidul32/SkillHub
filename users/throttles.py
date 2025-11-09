from rest_framework.throttling import SimpleRateThrottle

class LoginRateThrottle(SimpleRateThrottle):
    scope = 'login'
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None
        # rate-limit by IP
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
