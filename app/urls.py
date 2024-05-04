from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('qr_codes', views.qr_code_check, name='qr_code_check'),
]