# Generated by Django 5.0.4 on 2024-05-04 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_jadwal_kelas_akun_qr_hash_absensi_akun_kelas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jadwal',
            name='masuk',
        ),
        migrations.RemoveField(
            model_name='jadwal',
            name='pulang',
        ),
        migrations.AddField(
            model_name='jadwal',
            name='nama',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='jadwal',
            name='waktu',
            field=models.TimeField(default='06:00'),
        ),
    ]
