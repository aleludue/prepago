# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils import timezone


class Socio(models.Model):
    fk_fields = ('nroSocio', 'razonSocial')
    LOCALIDAD_CHOICES = ((1, 'Brinkmann'),
                         (2, 'Seeber'),
                         (3, 'Col. Vignaud'))

    nroSocio = models.PositiveIntegerField(unique=True, help_text="Número de socio.")
    razonSocial = models.CharField(max_length=140, help_text="Razón social o nombre y apellido del usuario.")
    domicilio = models.CharField(max_length=100,
                                 help_text="Domicilio principal del socio, luego cada terreno tendrá el suyo.")
    telefono = models.CharField(max_length=15, blank=True, help_text="Teléfono de contacto. <b>Opcional.</b>")
    fechaCreacion = models.DateField(auto_now_add=True)
    localidad = models.IntegerField(choices=LOCALIDAD_CHOICES, default=1,
                                    help_text="Localidad de residencia del socio.")
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.fk_display

    @property
    def fk_display(self):
        return '%s - %s' % (self.nroSocio, self.razonSocial)



class Terreno(models.Model):
    CONDICION_IVA_CHOICES = (('RINS', 'Responsable Inscripto'),
                             ('MONO', 'Monotributo'),
                             ('CFIN', 'Consumidor Final'),
                             ('EXEN', 'Exento'),
                             ('NOCA', 'No Categorizado'))

    socio = models.ForeignKey(Socio, help_text="Socio propietario del terreno.", verbose_name="")
    nroTerreno = models.CharField(unique=True, max_length=10, help_text="Número de terreno.")
    domicilio = models.CharField(max_length=100, help_text="Domicilio del terreno.")
    condicionIva = models.CharField(max_length=4, choices=CONDICION_IVA_CHOICES,
                                    help_text="Condicion de iva del terreno.")
    nroMedidorEnergia = models.CharField(max_length=30, help_text="Número de serie del medidor.")
    activo = models.BooleanField(default=True, help_text="Estado del terreno.")
    cargoConsumoAgua = models.BooleanField(default=True, help_text="Cargo por consumo de agua.")
    tarifa = models.ForeignKey('Tarifa', help_text="Tarifa aplicada al terreno.", verbose_name="")

    def __unicode__(self):
        return self.nroTerreno


class RecambioMedidor(models.Model):
    terreno = models.ForeignKey(Terreno)
    fecha = models.DateField(default=timezone.now)
    nroMedidor = models.CharField(max_length=30)

    def __unicode__(self):
        return '%s-%s' % (self.terreno, self.nroMedidor)


class Tarifa(models.Model):
    nombre = models.CharField(max_length=30, help_text="Nombre de la tarifa.")

    def __unicode__(self):
        return self.nombre


class EscalonesEnergia(models.Model):
    tarifa = models.ForeignKey(Tarifa, help_text="Tarifa a la que se aplicara el escalon energetico.")
    desde = models.IntegerField(help_text="Valor base del escalon.")
    hasta = models.IntegerField(help_text="Valor final del escalon.")
    valor = models.FloatField(help_text="Costo en pesos de los intervalos ingresados en el escalon.")

    def __unicode__(self):
        return '%s - %s a %s' % (self.tarifa, self.desde, self.hasta)


class Items(models.Model):
    TIPOS_CHOICES = (('FIJ', 'Fijo'),
                     ('VAR', 'Variable'))

    APLICACION_CHOICES = (('CF', 'Cargo Fijo'),
                          ('EN', 'Energia'))

    nombre = models.CharField(max_length=60, help_text="Nombre del item")
    tipo = models.CharField(max_length=3, choices=TIPOS_CHOICES, help_text="Tipo de valor del item, porcentual o fijo")
    aplicacion = models.CharField(max_length=2, choices=APLICACION_CHOICES, help_text="Área de aplicación del item")
    valor = models.FloatField(help_text="Valor del item")
    tarifa = models.ManyToManyField(Tarifa, through='Gravamen')
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre


class Gravamen(models.Model):
    IVA_CHOICES = (('IVA21', 'IVA 21%'),
                   ('IVA27', 'IVA 27%'),
                   ('NOGRA', 'No Gravado'),
                   ('EXENT', 'Exento'))

    tarifa = models.ForeignKey(Tarifa)
    item = models.ForeignKey(Items)
    iva = models.CharField(max_length=5, choices=IVA_CHOICES)


class Cesp(models.Model):
    nroCesp = models.CharField(unique=True, max_length=50, help_text="Número de CESP.")
    fecha = models.DateField(help_text="Fecha de validez del número CESP ingresado.")

    def __unicode__(self):
        return self.nroCesp


class Factura(models.Model):
    nroFactura = models.CharField(max_length=50, unique=True)
    fecha = models.DateField(auto_now_add=True)
    nroTerreno = models.ForeignKey(Terreno)
    importe = models.FloatField()
    cesp = models.ForeignKey(Cesp)
    tarifa = models.ForeignKey(Tarifa)
    items = models.ManyToManyField(Items, through='Factura_Items')

    def __unicode__(self):
        return self.nroFactura


class Factura_Items(models.Model):
    nroFactura = models.ForeignKey(Factura)
    item = models.ForeignKey(Items)
