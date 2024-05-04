from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import hashlib
# Create your models here.

class Akun(models.Model):
    '''Model definition for Akun.'''
    name = models.CharField(max_length=50)
    nisn = models.PositiveIntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(200)])
    
    class Meta:
        '''Meta definition for Akun.'''

        verbose_name = 'Akun'
        verbose_name_plural = 'Akuns'

    def generate_hash(self):
        # Using hashlib to generate a SHA-256 hash
        text_to_hash = f"{self.name}{self.nisn}"
        hash_object = hashlib.sha256(text_to_hash.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig
    
    def __str__(self):
        return self.name