from django.shortcuts import render
from django.http import JsonResponse

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .helpers import link_callback
from .models import Akun

# View


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


def render_pdf_view(request):
    template_path = 'qr_pdf.html'

    akun_instance = Akun.objects.first()  # Or retrieve it based on some condition

    # Generate the hash
    qr_code_hash = akun_instance.generate_hash()

    context = {'qr_code': qr_code_hash}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=lambda uri, rel: link_callback(uri, rel, request))

    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
