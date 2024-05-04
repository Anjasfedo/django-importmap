from django.shortcuts import render
from django.http import JsonResponse

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from .helpers import link_callback
from .models import Akun, Jadwal, Absensi

from django.utils import timezone

# View


def index(request):
    akun_instance = Akun.objects.first()

    qr_code_hash = akun_instance.qr_hash

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

        # Check if QR data has already been checked
        if request.session['qr_data_checked'] == False:
            # Store the fact that the QR data has been checked in the session
            request.session['qr_data_checked'] = True

            if qr_data == qr_code_hash:
                return JsonResponse({'message': 'QR code data received successfully', 'data': qr_data, 'type': 'success'}, status=200)
            else:
                return JsonResponse({'message': 'QR code data false', 'data': qr_data, 'type': 'failed'}, status=200)

        else:

            request.session['qr_data_checked'] = False
            return JsonResponse({'message': 'QR code data already checked', 'data': qr_data, 'type': 'already_checked'}, status=200)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=400)


def mark_attendance(request, hash_value):
    akun = Akun.get_akun_by_hash(hash_value)
    if akun:
        now = timezone.now().time()
        closest_jadwal = Jadwal.objects.filter(
            start_time__gte=now).order_by('start_time').first()
        if closest_jadwal:
            absensi = Absensi(akun=akun, jadwal=closest_jadwal)
            absensi.calculate_status()
            absensi.save()
            return HttpResponse(f"Absensi marked for {akun.user.username} in {closest_jadwal}")
        else:
            return HttpResponse("No upcoming jadwals found")
    else:
        return HttpResponse("Akun not found")

# Render PDF

def render_pdf_view(request):
    template_path = 'qr_pdf.html'

    akun_instance = Akun.objects.first()  # Or retrieve it based on some condition

    # Ensure akun_instance exists before proceeding
    if akun_instance:
        # Get the name and NISN from the Akun instance
        name = akun_instance.name
        nisn = akun_instance.nisn
        # Generate the hash
        qr_code_hash = akun_instance.generate_hash()

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
