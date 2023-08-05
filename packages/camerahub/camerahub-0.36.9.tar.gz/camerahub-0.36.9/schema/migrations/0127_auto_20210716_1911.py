# Generated by Django 2.2.23 on 2021-07-16 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0125_auto_20210517_2102'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='accessory',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_acce_owner_i_064684_idx'),
        ),
        migrations.AddIndex(
            model_name='archive',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_arch_owner_i_1e0470_idx'),
        ),
        migrations.AddIndex(
            model_name='battery',
            index=models.Index(fields=['slug'], name='schema_batt_slug_5185f7_idx'),
        ),
        migrations.AddIndex(
            model_name='bulkfilm',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_bulk_owner_i_4c6b52_idx'),
        ),
        migrations.AddIndex(
            model_name='camera',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_came_owner_i_131481_idx'),
        ),
        migrations.AddIndex(
            model_name='cameramodel',
            index=models.Index(fields=['slug'], name='schema_came_slug_76fba7_idx'),
        ),
        migrations.AddIndex(
            model_name='developer',
            index=models.Index(fields=['slug'], name='schema_deve_slug_208c0a_idx'),
        ),
        migrations.AddIndex(
            model_name='enlarger',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_enla_owner_i_f376cb_idx'),
        ),
        migrations.AddIndex(
            model_name='enlargermodel',
            index=models.Index(fields=['slug'], name='schema_enla_slug_cdd708_idx'),
        ),
        migrations.AddIndex(
            model_name='film',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_film_owner_i_262269_idx'),
        ),
        migrations.AddIndex(
            model_name='filmstock',
            index=models.Index(fields=['slug'], name='schema_film_slug_77941c_idx'),
        ),
        migrations.AddIndex(
            model_name='flash',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_flas_owner_i_90ed5d_idx'),
        ),
        migrations.AddIndex(
            model_name='flashmodel',
            index=models.Index(fields=['slug'], name='schema_flas_slug_35f243_idx'),
        ),
        migrations.AddIndex(
            model_name='lens',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_lens_owner_i_ef47ee_idx'),
        ),
        migrations.AddIndex(
            model_name='lensmodel',
            index=models.Index(fields=['slug'], name='schema_lens_slug_1b7268_idx'),
        ),
        migrations.AddIndex(
            model_name='manufacturer',
            index=models.Index(fields=['slug'], name='schema_manu_slug_fd5a47_idx'),
        ),
        migrations.AddIndex(
            model_name='manufacturer',
            index=models.Index(fields=['country', 'country'], name='schema_manu_country_abce90_idx'),
        ),
        migrations.AddIndex(
            model_name='mount',
            index=models.Index(fields=['slug'], name='schema_moun_slug_d93c9e_idx'),
        ),
        migrations.AddIndex(
            model_name='mountadapter',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_moun_owner_i_56f606_idx'),
        ),
        migrations.AddIndex(
            model_name='negative',
            index=models.Index(fields=['slug'], name='schema_nega_slug_146056_idx'),
        ),
        migrations.AddIndex(
            model_name='negative',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_nega_owner_i_a88607_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_orde_owner_i_c53670_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_pers_owner_i_e452fe_idx'),
        ),
        migrations.AddIndex(
            model_name='print',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_prin_owner_i_235fbb_idx'),
        ),
        migrations.AddIndex(
            model_name='teleconverter',
            index=models.Index(fields=['owner', 'id_owner'], name='schema_tele_owner_i_80ab0e_idx'),
        ),
        migrations.AddIndex(
            model_name='teleconvertermodel',
            index=models.Index(fields=['slug'], name='schema_tele_slug_6eab52_idx'),
        ),
        migrations.AddIndex(
            model_name='toner',
            index=models.Index(fields=['slug'], name='schema_tone_slug_3724e1_idx'),
        ),
    ]
