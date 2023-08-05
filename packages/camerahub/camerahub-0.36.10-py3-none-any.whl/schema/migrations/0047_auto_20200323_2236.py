# Generated by Django 2.2 on 2020-03-23 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schema', '0046_auto_20200323_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='lensmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='lensmodel',
            name='created_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False,
                                                                       null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lensmodel_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lensmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='lensmodel',
            name='updated_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True,
                                                                       on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='lensmodel_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cameramodel',
            name='created_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, editable=False,
                                                                       null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cameramodel_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cameramodel',
            name='updated_by',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True,
                                                                       on_delete=django.db.models.deletion.CASCADE, on_update=True, related_name='cameramodel_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
