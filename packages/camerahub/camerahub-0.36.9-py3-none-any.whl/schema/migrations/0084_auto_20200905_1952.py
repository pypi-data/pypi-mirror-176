# Generated by Django 2.2.14 on 2020-09-05 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0083_auto_20200904_2154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cameramodel',
            old_name='power_drive',
            new_name='internal_power_drive',
        ),
        migrations.RenameField(
            model_name='historicalcameramodel',
            old_name='power_drive',
            new_name='internal_power_drive',
        ),
    ]
