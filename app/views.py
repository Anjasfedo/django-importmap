from django.shortcuts import render
from django.http import JsonResponse

from .models import Akun


def index(request):
    akun_instance = Akun.objects.first()
    
    qr_code_hash = akun_instance.generate_hash()
    
    context = {
        'qr_code': qr_code_hash
    }

    return render(request, 'index.html', context)


def qr_code_check(request):
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')

        akun_instance = Akun.objects.first()  # Or retrieve it based on some condition

        # Generate the hash
        qr_code_hash = akun_instance.generate_hash()

        if qr_data == qr_code_hash:
            return JsonResponse({'message': 'QR code data received successfully', 'data': qr_data, 'type': 'success'}, status=200)
        else:
            return JsonResponse({'message': 'QR code data false', 'data': qr_data, 'type': 'failed'}, status=200)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)
