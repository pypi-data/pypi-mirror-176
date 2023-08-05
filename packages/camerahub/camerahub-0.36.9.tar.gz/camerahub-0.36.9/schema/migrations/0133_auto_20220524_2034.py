# Generated by Django 3.2.13 on 2022-05-24 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0132_auto_20220524_2017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalcameramodel',
            name='battery_type',
        ),
        migrations.RemoveField(
            model_name='historicalcameramodel',
            name='fastest_shutter_speed',
        ),
        migrations.RemoveField(
            model_name='historicalcameramodel',
            name='format',
        ),
        migrations.RemoveField(
            model_name='historicalcameramodel',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalcameramodel',
            name='lens_manufacturer',
        ),
        migrations.RemoveField(
            model_name='historicalcameramodel',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='historicalcameramodel',
            name='mount',
        ),
        migrations.RemoveField(
            model_name='historicalcameramodel',
            name='negative_size',
        ),
        migrations.RemoveField(
            model_name='historicalcameramodel',
            name='slowest_shutter_speed',
        ),
        migrations.RemoveField(
            model_name='historicalcameramodel',
            name='x_sync',
        ),
        migrations.RemoveField(
            model_name='historicaldeveloper',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaldeveloper',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='historicalenlargermodel',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalenlargermodel',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='historicalenlargermodel',
            name='negative_size',
        ),
        migrations.RemoveField(
            model_name='historicalfilmstock',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalfilmstock',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='historicalfilmstock',
            name='process',
        ),
        migrations.RemoveField(
            model_name='historicalflashmodel',
            name='battery_type',
        ),
        migrations.RemoveField(
            model_name='historicalflashmodel',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalflashmodel',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='historicalformat',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicallensmodel',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicallensmodel',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='historicallensmodel',
            name='mount',
        ),
        migrations.RemoveField(
            model_name='historicallensmodel',
            name='negative_size',
        ),
        migrations.RemoveField(
            model_name='historicalmanufacturer',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalmount',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalmount',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='historicalnegativesize',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalpaperstock',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalpaperstock',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='historicalprocess',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalteleconvertermodel',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalteleconvertermodel',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='historicalteleconvertermodel',
            name='mount',
        ),
        migrations.RemoveField(
            model_name='historicaltoner',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicaltoner',
            name='manufacturer',
        ),
        migrations.DeleteModel(
            name='HistoricalBattery',
        ),
        migrations.DeleteModel(
            name='HistoricalCameraModel',
        ),
        migrations.DeleteModel(
            name='HistoricalDeveloper',
        ),
        migrations.DeleteModel(
            name='HistoricalEnlargerModel',
        ),
        migrations.DeleteModel(
            name='HistoricalFilmStock',
        ),
        migrations.DeleteModel(
            name='HistoricalFlashModel',
        ),
        migrations.DeleteModel(
            name='HistoricalFormat',
        ),
        migrations.DeleteModel(
            name='HistoricalLensModel',
        ),
        migrations.DeleteModel(
            name='HistoricalManufacturer',
        ),
        migrations.DeleteModel(
            name='HistoricalMount',
        ),
        migrations.DeleteModel(
            name='HistoricalNegativeSize',
        ),
        migrations.DeleteModel(
            name='HistoricalPaperStock',
        ),
        migrations.DeleteModel(
            name='HistoricalProcess',
        ),
        migrations.DeleteModel(
            name='HistoricalTeleconverterModel',
        ),
        migrations.DeleteModel(
            name='HistoricalToner',
        ),
    ]
