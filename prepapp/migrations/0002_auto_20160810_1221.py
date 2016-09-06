# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('prepapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarifa',
            name='terreno',
        ),
        migrations.AddField(
            model_name='terreno',
            name='tarifa',
            field=models.ForeignKey(default=1, to='prepapp.Tarifa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recambiomedidor',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2016, 8, 10, 15, 20, 11, 820000, tzinfo=utc)),
        ),
    ]
