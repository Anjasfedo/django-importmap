# Generated by Django 5.0.4 on 2024-05-04 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_absensi_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='akun',
            name='kelas',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.kelas'),
        ),
    ]
