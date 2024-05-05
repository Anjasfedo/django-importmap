from django import forms
from .models import Akun

class AkunForm(forms.ModelForm):
    class Meta:
        model = Akun
        fields = '__all__'
        exclude = ['qr_hash']
        