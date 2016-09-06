# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('prepapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recambiomedidor',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
