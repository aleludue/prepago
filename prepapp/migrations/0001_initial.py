# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cesp',
            fields=[
                ('nroCesp', models.IntegerField(serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='EscalonesEnergia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desde', models.IntegerField()),
                ('hasta', models.IntegerField()),
                ('valor', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('nroFactura', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('importe', models.FloatField()),
                ('cesp', models.ForeignKey(to='prepapp.Cesp')),
            ],
        ),
        migrations.CreateModel(
            name='Factura_Items',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gravamen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iva', models.CharField(max_length=5, choices=[('IVA21', 'IVA 21%'), ('IVA27', 'IVA 27%'), ('NOGRA', 'No Gravado'), ('EXENT', 'Exento')])),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=60)),
                ('tipo', models.CharField(max_length=3, choices=[('FIJ', 'Fijo'), ('VAR', 'Variable')])),
                ('aplicacion', models.CharField(max_length=2, choices=[('CF', 'Cargo Fijo'), ('EN', 'Energia')])),
                ('valor', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RecambioMedidor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=datetime.datetime(2016, 8, 10, 14, 3, 55, 538000, tzinfo=utc))),
                ('nroMedidor', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Socio',
            fields=[
                ('nroSocio', models.IntegerField(serialize=False, primary_key=True)),
                ('razonSocial', models.CharField(max_length=140)),
                ('domicilio', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('fechaCreacion', models.DateField(auto_now_add=True)),
                ('localidad', models.IntegerField(choices=[(1, 'Brinkmann'), (2, 'Seeber'), (3, 'Col. Vignaud')])),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Terreno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nroTerreno', models.CharField(max_length=10)),
                ('domicilio', models.CharField(max_length=100)),
                ('condicionIva', models.CharField(max_length=4, choices=[('RINS', 'Responsable Inscripto'), ('MONO', 'Monotributo'), ('CFIN', 'Consumidor Final'), ('EXEN', 'Exento'), ('NOCA', 'No Categorizado')])),
                ('nroMedidorEnergia', models.CharField(max_length=30)),
                ('activo', models.BooleanField(default=True)),
                ('cargoConsumoAgua', models.BooleanField(default=True)),
                ('socio', models.ForeignKey(to='prepapp.Socio')),
            ],
        ),
        migrations.AddField(
            model_name='tarifa',
            name='terreno',
            field=models.ForeignKey(to='prepapp.Terreno'),
        ),
        migrations.AddField(
            model_name='recambiomedidor',
            name='terreno',
            field=models.ForeignKey(to='prepapp.Terreno'),
        ),
        migrations.AddField(
            model_name='items',
            name='tarifa',
            field=models.ManyToManyField(to='prepapp.Tarifa', through='prepapp.Gravamen'),
        ),
        migrations.AddField(
            model_name='gravamen',
            name='item',
            field=models.ForeignKey(to='prepapp.Items'),
        ),
        migrations.AddField(
            model_name='gravamen',
            name='tarifa',
            field=models.ForeignKey(to='prepapp.Tarifa'),
        ),
        migrations.AddField(
            model_name='factura_items',
            name='item',
            field=models.ForeignKey(to='prepapp.Items'),
        ),
        migrations.AddField(
            model_name='factura_items',
            name='nroFactura',
            field=models.ForeignKey(to='prepapp.Factura'),
        ),
        migrations.AddField(
            model_name='factura',
            name='items',
            field=models.ManyToManyField(to='prepapp.Items', through='prepapp.Factura_Items'),
        ),
        migrations.AddField(
            model_name='factura',
            name='nroTerreno',
            field=models.ForeignKey(to='prepapp.Terreno'),
        ),
        migrations.AddField(
            model_name='factura',
            name='tarifa',
            field=models.ForeignKey(to='prepapp.Tarifa'),
        ),
        migrations.AddField(
            model_name='escalonesenergia',
            name='tarifa',
            field=models.ForeignKey(to='prepapp.Tarifa'),
        ),
    ]
