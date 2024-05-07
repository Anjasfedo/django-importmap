from django.contrib import admin
from .models import Akun


@admin.register(Akun)
class ModelAdmin(admin.ModelAdmin):

    def get_fieldsets(self, request, obj=None):
        if request.user.groups.filter(name='admin').exists():
            return self.admin_fieldsets
        elif request.user.groups.filter(name='ademin').exists():
            return self.ademin_fieldsets

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    ademin_fieldsets = (
        (None, {'fields': ('name', 'nisn')}),
    )

    admin_fieldsets = (
        (None, {'fields': ('name', 'nisn')}),
        (None, {'fields': ('kelas', 'qr_hash')}),
    )

    def get_list_display(self, request):
        if request.user.groups.filter(name='admin').exists():
            return ('name', 'nisn', 'kelas', 'qr_hash')
        elif request.user.groups.filter(name='ademin').exists():
            return ('name', 'nisn', 'kelas')
