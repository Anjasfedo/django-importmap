# Generated by Django 5.0.4 on 2024-05-04 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_jadwal_masuk_remove_jadwal_pulang_jadwal_nama_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='absensi',
            unique_together={('akun', 'jadwal', 'date')},
        ),
    ]
