from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from ipgeolocation import IpGeolocationAPI

from .models import RequestLog, BlockedIP

class IPLoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        ip = request.META.get('REMOTE_ADDR')

        # Blocked IP check
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access Denied")

        # Geolocation with cache (24 hours)
        geo_data = cache.get(ip)
        if not geo_data:
            api = IpGeolocationAPI()
            geo_data = api.get(ip)
            cache.set(ip, geo_data, 86400)

        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            country=geo_data.get('country_name') if geo_data else None,
            city=geo_data.get('city') if geo_data else None
        )
