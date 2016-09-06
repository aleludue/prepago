# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('prepapp', '0002_auto_20160810_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recambiomedidor',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 8, 10, 15, 28, 39, 552000, tzinfo=utc)),
        ),
    ]
