from __future__ import unicode_literals
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('schema', '0116_auto_20201216_2013'),
    ]
    operations = [
        migrations.RunPython(
            migrations.RunPython.noop, reverse_code=migrations.RunPython.noop),

    ]
