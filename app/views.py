from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def index(request):
    context = {}
    
    return render(request, 'index.html', context)

def qr_code_create(request):
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')
        # Lakukan sesuatu dengan qr_data, seperti menyimpannya ke database
        # Misalnya:
        # QRCode.objects.create(data=qr_data)
        if qr_data == 'Quo veniam ducimus312312323':
            return JsonResponse({'message': 'QR code data received successfully', 'data': qr_data, 'type': 'success'}, status=200)
        else:
            return JsonResponse({'message': 'QR code data false', 'data': qr_data, 'type': 'failed'}, status=200)
            
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)