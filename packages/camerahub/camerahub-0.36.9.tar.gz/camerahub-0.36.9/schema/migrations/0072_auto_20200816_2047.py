# Generated by Django 2.2.14 on 2020-08-16 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0071_auto_20200813_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallensmodel',
            name='lens_type',
            field=models.CharField(blank=True, choices=[('Super telephoto', 'Super telephoto'), ('Medium telephoto', 'Medium telephoto'), ('Short telephoto', 'Short telephoto'), ('Normal', 'Normal'), ('Wide angle', 'Wide angle'), ('Super wide angle', 'Super wide angle'), ('Fisheye', 'Fisheye')], help_text='Type of lens based on its angle of view', max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='lensmodel',
            name='lens_type',
            field=models.CharField(blank=True, choices=[('Super telephoto', 'Super telephoto'), ('Medium telephoto', 'Medium telephoto'), ('Short telephoto', 'Short telephoto'), ('Normal', 'Normal'), ('Wide angle', 'Wide angle'), ('Super wide angle', 'Super wide angle'), ('Fisheye', 'Fisheye')], help_text='Type of lens based on its angle of view', max_length=16, null=True),
        ),
    ]
