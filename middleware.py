# ip_tracking/middleware.py
from .models import RequestLog
from django.utils.deprecation import MiddlewareMixin

class IPLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path
        )
