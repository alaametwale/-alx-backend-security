from django.http import HttpResponse
from ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request):
    return HttpResponse("Login endpoint (rate limited)")
