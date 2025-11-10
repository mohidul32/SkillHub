import time
from users.models import ActivityLog

class ActivityLogMiddleware:
    """
    Logs user requests (path, method, duration, IP, status).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)
        duration = round(time.time() - start_time, 3)

        user = request.user if request.user.is_authenticated else None
        ip = self.get_client_ip(request)

        ActivityLog.objects.create(
            user=user,
            path=request.path,
            method=request.method,
            status_code=response.status_code,
            ip_address=ip,
            duration=duration
        )

        # print(f"[LOG] {user} → {request.method} {request.path} ({response.status_code}) - {duration}s")

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
