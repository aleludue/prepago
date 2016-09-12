# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgrupacionDeItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desde', models.IntegerField()),
                ('hasta', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AsociacionItemAgrupacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iva', models.CharField(max_length=5, choices=[('IVA21', 'IVA 21%'), ('IVA27', 'IVA 27%'), ('NOGRA', 'No Gravado'), ('EXENT', 'Exento')])),
                ('valor', models.DecimalField(max_digits=10, decimal_places=5)),
                ('agrupacion', models.ForeignKey(to='prepapp.AgrupacionDeItems')),
            ],
        ),
        migrations.CreateModel(
            name='Cesp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nroCesp', models.CharField(help_text='N\xfamero de CESP.', unique=True, max_length=50)),
                ('fecha', models.DateField(help_text='Fecha de validez del n\xfamero CESP ingresado.')),
            ],
        ),
        migrations.CreateModel(
            name='Escalones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desde', models.IntegerField(help_text='Valor base del escalon.')),
                ('hasta', models.IntegerField(help_text='Valor final del escalon.')),
                ('valor', models.FloatField(help_text='Costo en pesos de los intervalos ingresados en el escalon.')),
                ('asociacion', models.ForeignKey(help_text='Asociacion a la que se aplicara el escalon.', to='prepapp.AsociacionItemAgrupacion')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nroFactura', models.CharField(unique=True, max_length=50)),
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
            name='Items',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=60)),
                ('tipo', models.CharField(max_length=3, choices=[('FIJ', 'Fijo'), ('VAR', 'Variable'), ('ESC', 'Escalonado')])),
                ('aplicacion', models.CharField(max_length=2, choices=[('CF', 'Cargo Fijo'), ('EN', 'Energia')])),
                ('servicios', models.CharField(max_length=4, choices=[('ENER', 'Energia El\xe9ctrica'), ('AGUA', 'Agua Corriente'), ('CLOA', 'Cloacas'), ('SERV', 'Servicios Sociales'), ('ACUE', 'A cuenta de terceros')])),
                ('activo', models.BooleanField(default=True)),
                ('base', models.BooleanField(default=False)),
                ('requerido', models.BooleanField(default=False)),
                ('tarifa', models.ManyToManyField(to='prepapp.AgrupacionDeItems', through='prepapp.AsociacionItemAgrupacion')),
            ],
        ),
        migrations.CreateModel(
            name='RecambioMedidor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('nroMedidor', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Socio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nroSocio', models.PositiveIntegerField(help_text='N\xfamero de socio.', unique=True)),
                ('razonSocial', models.CharField(help_text='Raz\xf3n social o nombre y apellido del usuario.', max_length=140)),
                ('domicilio', models.CharField(help_text='Domicilio principal del socio, luego cada terreno tendr\xe1 el suyo.', max_length=100)),
                ('telefono', models.CharField(help_text='Tel\xe9fono de contacto. <b>Opcional.</b>', max_length=15, blank=True)),
                ('fechaCreacion', models.DateField(auto_now_add=True)),
                ('localidad', models.IntegerField(default=1, help_text='Localidad de residencia del socio.', choices=[(1, 'Brinkmann'), (2, 'Seeber'), (3, 'Col. Vignaud')])),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(help_text='Nombre de la tarifa.', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Terreno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nroTerreno', models.CharField(help_text='N\xfamero de terreno.', unique=True, max_length=10)),
                ('domicilio', models.CharField(help_text='Domicilio del terreno.', max_length=100)),
                ('condicionIva', models.CharField(help_text='Condicion de iva del terreno.', max_length=4, choices=[('RINS', 'Responsable Inscripto'), ('MONO', 'Monotributo'), ('CFIN', 'Consumidor Final'), ('EXEN', 'Exento'), ('NOCA', 'No Categorizado')])),
                ('nroMedidorEnergia', models.CharField(help_text='N\xfamero de serie del medidor.', max_length=30)),
                ('activo', models.BooleanField(default=True, help_text='Estado del terreno.')),
                ('cargoConsumoAgua', models.BooleanField(default=True, help_text='Cargo por consumo de agua.')),
                ('socio', models.ForeignKey(verbose_name='', to='prepapp.Socio', help_text='Socio propietario del terreno.')),
                ('tarifa', models.ForeignKey(verbose_name='', to='prepapp.Tarifa', help_text='Tarifa aplicada al terreno.')),
            ],
        ),
        migrations.AddField(
            model_name='recambiomedidor',
            name='terreno',
            field=models.ForeignKey(to='prepapp.Terreno'),
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
            model_name='asociacionitemagrupacion',
            name='item',
            field=models.ForeignKey(to='prepapp.Items'),
        ),
        migrations.AddField(
            model_name='agrupaciondeitems',
            name='tarifa',
            field=models.ForeignKey(help_text='Tarifa asociada a esta agrupacion', to='prepapp.Tarifa'),
        ),
    ]
