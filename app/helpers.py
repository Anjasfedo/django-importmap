from django.template.loader import render_to_string

from django.http import HttpRequest

def get_current_host(request: HttpRequest) -> str:
    scheme = request.is_secure() and "https" or "http"
    return f'{scheme}://{request.get_host()}/'


def link_callback(uri, rel, request):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    import os
    from django.conf import settings

    HOSTNAME = get_current_host(request)

    qr_code_image_path = '/qr-code-image/'  # QR code image path
    static_url = settings.STATIC_URL          # Typically /static/

    if uri.startswith(qr_code_image_path):
        # If URI starts with /qr-code-image/, return the full URI with the host
        return f"{HOSTNAME}{uri}"
    elif uri.startswith(static_url):
        # If URI starts with /static/, construct the absolute path for static files
        path = uri.replace(static_url, "")
        return os.path.join(settings.STATIC_ROOT, path)

    # If URI doesn't start with /qr-code-image/ or /static/, return the full URI with the host
    return f"{HOSTNAME}{uri}"
