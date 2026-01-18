from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    one_hour_ago = now() - timedelta(hours=1)
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    ip_counter = {}

    for log in logs:
        ip_counter[log.ip_address] = ip_counter.get(log.ip_address, 0) + 1

        if log.path in ['/admin/', '/login/']:
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                reason=f"Accessed sensitive path: {log.path}"
            )

    for ip, count in ip_counter.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason="Exceeded 100 requests/hour"
            )
