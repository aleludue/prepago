# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('prepapp', '0003_auto_20160810_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cesp',
            name='nroCesp',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='recambiomedidor',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 8, 10, 15, 41, 39, 949000, tzinfo=utc)),
        ),
    ]
