from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import hashlib
import datetime

from .helpers import max_value_current_year, get_current_time

# Create your models here.

SECRET_KEY = 'f46facdb5eec53ed5e8ec71490e8e1b030ea7dcd449f06653305ab4a1df949eb'

class Jadwal(models.Model):
    masuk = models.TimeField(default='08:00')  # Default value for start time is '08:00' (morning)
    pulang = models.TimeField(default='17:00')  # Default value for finish time is '17:00' (afternoon)
    # Other fields for schedule
    
class Kelas(models.Model):
    '''Model definition for Class.'''
    name = models.CharField(max_length=20)
    year = models.IntegerField(
        validators=[MinValueValidator(1984), max_value_current_year], unique=True)

    class Meta:
        '''Meta definition for Class.'''

        verbose_name = 'Class'
        verbose_name_plural = 'Classs'

    def __str__(self):
        return str(self.year)


class Akun(models.Model):
    '''Model definition for Akun.'''
    name = models.CharField(max_length=50)
    nisn = models.PositiveIntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(200)])
    # One to one with User
    kelas = models.OneToOneField(Kelas, on_delete=models.CASCADE, null=True)
    qr_hash = models.CharField(max_length=255, null=True)

    class Meta:
        '''Meta definition for Akun.'''

        verbose_name = 'Akun'
        verbose_name_plural = 'Akuns'

    def generate_hash(self):
        # Using hashlib to generate a SHA-256 hash
        text_to_hash = f"{self.name}{SECRET_KEY}"
        hash_object = hashlib.sha256(text_to_hash.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig
    
    def get_akun_by_hash(cls, hash_value):
        try:
            return cls.objects.get(qr_hash=hash_value)
        except cls.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        # Override save method to update qr_hash when saving the object
        self.qr_hash = self.generate_hash()  # Generate hash when saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Absensi(models.Model):
    akun = models.ForeignKey(Akun, on_delete=models.CASCADE)
    jadwal = models.ForeignKey(Jadwal, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True) 
    time = models.TimeField(default=get_current_time)
    status = models.CharField(max_length=10, choices=[
                              ('hadir', 'Hadir'), ('absen', 'Absen')])

    def calculate_status(self):
        current_time = datetime.datetime.now().time()
        if self.jadwal.masuk <= current_time <= self.jadwal.pulang:
            self.status = 'absen'
        else:
            self.status = 'hadir'
