from django.http import JsonResponse


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request path is for the QR code image URL
        if request.path.startswith('/qr-code-image/'):
            # If the user is not authenticated, return JSON response indicating authentication is required
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=401)
        # Allow the request to proceed to the next middleware or view
        return self.get_response(request)
