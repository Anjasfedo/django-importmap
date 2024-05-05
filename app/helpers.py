from django.http import HttpRequest
import datetime
from django.core.validators import MaxValueValidator

def get_current_host(request: HttpRequest) -> str:
    scheme = request.is_secure() and "https" or "http"
    return f'{scheme}://{request.get_host()}/'

def link_callback(uri, rel, request):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    HOSTNAME = get_current_host(request)

    return f"{HOSTNAME}{uri}"


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def get_current_time():
    return datetime.datetime.now().time()
