from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from xhtml2pdf import pisa

from .helpers import link_callback
from .models import Akun, Jadwal, Absensi
# View


def index(request, jadwal):
    # Get the Jadwal object based on the jadwal parameter
    jadwal_object = get_object_or_404(Jadwal, nama__iexact=jadwal)

    akun_instance = Akun.objects.get(pk=2)
    qr_code_hash = akun_instance.qr_hash

    context = {
        'qr_code': qr_code_hash,
        'jadwal': jadwal_object
    }

    return render(request, 'index.html', context)


def qr_code_check(request):
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data')
        jadwal_name = request.POST.get('jadwal')

        akun = Akun.get_akun_by_hash(qr_data)

        if akun:
            now_jadwal = Jadwal.objects.filter(
                nama__iexact=jadwal_name).latest('waktu')

            if now_jadwal:
                try:
                    absensi = Absensi(akun=akun, jadwal=now_jadwal)
                    absensi.save()
                    return JsonResponse({'message': f'QR code data received successfully {now_jadwal}', 'data': qr_data, 'type': 'success'}, status=200)
                except IntegrityError:
                    return JsonResponse({'message': f'Absensi record already exists for this akun, jadwal, and date combination {now_jadwal}', 'type': 'failed'}, status=200)
            else:
                return JsonResponse({'message': 'Jadwal not found', 'type': 'failed'}, status=200)
        else:
            return JsonResponse({'message': 'Akun not found', 'type': 'failed'}, status=200)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)


# Render PDF

def render_pdf_view(request):
    template_path = 'qr_pdf.html'

    akun_instance = Akun.objects.get(pk=1)  # Or retrieve it based on some condition

    # Ensure akun_instance exists before proceeding
    if akun_instance:
        # Get the name and NISN from the Akun instance
        name = akun_instance.name
        nisn = akun_instance.nisn
        # Generate the hash
        qr_code_hash = akun_instance.qr_hash

        context = {
            'qr_code': qr_code_hash,
            'name': name,
            'nisn': nisn
        }

        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{name}.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=lambda uri, rel: link_callback(uri, rel, request))

        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        # Handle case where no Akun instance is found
        return HttpResponse('No Akun instance found')
