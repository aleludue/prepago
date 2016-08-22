# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.
from django.utils import timezone


class Socio(models.Model):
    LOCALIDAD_CHOICES = ((1, 'Brinkmann'),
                         (2, 'Seeber'),
                         (3, 'Col. Vignaud'))

    nroSocio = models.PositiveIntegerField(primary_key=True, help_text="Número de socio.")
    razonSocial = models.CharField(max_length=140, help_text="Razón social o nombre y apellido del usuario.")
    domicilio = models.CharField(max_length=100, help_text="Domicilio principal del socio, luego cada terreno tendrá el suyo.")
    telefono = models.CharField(max_length=15, blank=True, help_text="Teléfono de contacto. <b>Opcional.</b>")
    fechaCreacion = models.DateField(auto_now_add=True)
    localidad = models.IntegerField(choices=LOCALIDAD_CHOICES, default=1, help_text="Localidad de residencia del socio.")
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s - %s'%(self.nroSocio, self.razonSocial)

    class Admin:
        pass


class Terreno(models.Model):
    CONDICION_IVA_CHOICES = (('RINS', 'Responsable Inscripto'),
                             ('MONO', 'Monotributo'),
                             ('CFIN', 'Consumidor Final'),
                             ('EXEN', 'Exento'),
                             ('NOCA', 'No Categorizado'))

    socio = models.ForeignKey(Socio)
    nroTerreno = models.CharField(max_length=10)
    domicilio = models.CharField(max_length=100)
    condicionIva = models.CharField(max_length=4, choices=CONDICION_IVA_CHOICES)
    nroMedidorEnergia = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)
    cargoConsumoAgua = models.BooleanField(default=True)
    tarifa = models.ForeignKey('Tarifa')

    def __unicode__(self):
        return self.nroTerreno

    class Admin:
        pass

class RecambioMedidor(models.Model):
    terreno = models.ForeignKey(Terreno)
    fecha = models.DateField(default=timezone.now())
    nroMedidor = models.CharField(max_length=30)

    def __unicode__(self):
        return '%s - %s' % (self.terreno, self.nroMedidor)

    class Admin:
        pass

class Tarifa(models.Model):
    nombre = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nombre

    class Admin:
        pass

class EscalonesEnergia(models.Model):
    tarifa = models.ForeignKey(Tarifa)
    desde = models.IntegerField()
    hasta = models.IntegerField()
    valor = models.FloatField()

    def __unicode__(self):
        return '%s - %s a %s' % (self.tarifa, self.desde, self.hasta)

    class Admin:
        pass

class Items(models.Model):
    TIPOS_CHOICES = (('FIJ', 'Fijo'),
                    ('VAR', 'Variable'))

    APLICACION_CHOICES = (('CF', 'Cargo Fijo'),
                          ('EN', 'Energia'))

    nombre = models.CharField(max_length=60)
    tipo = models.CharField(max_length=3, choices=TIPOS_CHOICES)
    aplicacion = models.CharField(max_length=2, choices=APLICACION_CHOICES)
    valor = models.FloatField()
    tarifa = models.ManyToManyField(Tarifa, through='Gravamen')

    def __unicode__(self):
        return self.nombre

    class Admin:
        pass

class Gravamen(models.Model):
    IVA_CHOICES = (('IVA21', 'IVA 21%'),
                   ('IVA27', 'IVA 27%'),
                   ('NOGRA', 'No Gravado'),
                   ('EXENT', 'Exento'))

    tarifa = models.ForeignKey(Tarifa)
    item = models.ForeignKey(Items)
    iva = models.CharField(max_length=5, choices=IVA_CHOICES)

class Cesp(models.Model):
    nroCesp = models.CharField(primary_key=True, max_length=50)
    fecha = models.DateField()

    def __unicode__(self):
        return self.nroCesp

class Factura(models.Model):
    nroFactura = models.CharField(max_length=50, primary_key=True)
    fecha = models.DateField(auto_now_add=True)
    nroTerreno = models.ForeignKey(Terreno)
    importe = models.FloatField()
    cesp = models.ForeignKey(Cesp)
    tarifa = models.ForeignKey(Tarifa)
    items = models.ManyToManyField(Items, through='Factura_Items')

    def __unicode__(self):
        return self.nroFactura

    class Admin:
        pass

class Factura_Items(models.Model):
    nroFactura = models.ForeignKey(Factura)
    item = models.ForeignKey(Items)

