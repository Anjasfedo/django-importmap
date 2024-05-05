from django.contrib import admin

from .models import Akun, Jadwal, Absensi, Kelas
from .forms import AkunForm
# Register your models here.


class AkunAdmin(admin.ModelAdmin):
    form = AkunForm


# admin.site.register([Akun, Jadwal, Absensi, Kelas])
admin.site.register(Akun, AkunAdmin)
admin.site.register(Jadwal)
admin.site.register(Absensi)
admin.site.register(Kelas)
