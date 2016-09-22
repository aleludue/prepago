# coding=utf-8
from __future__ import unicode_literals

from decimal import Decimal
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
    nroMedidorAgua = models.CharField(max_length=30, help_text="Número de serie del medidor de agua.")
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


class AgrupacionDeItems(models.Model):
    tarifa = models.ForeignKey(Tarifa, help_text="Tarifa asociada a esta agrupacion", on_delete=models.CASCADE)
    desde = models.IntegerField()
    hasta = models.IntegerField()

    def __unicode__(self):
        return "%s: %s - %s" % (self.tarifa.nombre, self.desde, self.hasta)


class Items(models.Model):
    fk_fields = ('nombre',)
    TIPOS_CHOICES = (('FIJ', 'Fijo'),
                     ('VAR', 'Variable'),
                     ('ESC', 'Escalonado'))

    APLICACION_CHOICES = (('CF', 'Cargo Fijo'),
                          ('EN', 'Energia'))

    SERVICIOS = (('ENER', 'Energia Eléctrica'),
                 ('AGUA', 'Agua Corriente'),
                 ('CLOA', 'Cloacas'),
                 ('SERV', 'Servicios Sociales'),
                 ('ACUE', 'A cuenta de terceros'))

    ALIC_IVA = ((Decimal("0.00"), '0%'),
                (Decimal("10.50"), '10.5%'),
                (Decimal("21.00"), '21%'),
                (Decimal("27.00"), '27%'))

    nombre = models.CharField(max_length=60)
    tipo = models.CharField(max_length=3, choices=TIPOS_CHOICES, help_text='Tipo de item')
    aplicacion = models.CharField(max_length=2, choices=APLICACION_CHOICES, help_text='Ambito de aplicacion del Item')
    tarifa = models.ManyToManyField(AgrupacionDeItems, through='AsociacionItemAgrupacion')
    servicios = models.CharField(max_length=4, choices=SERVICIOS, help_text='Servicio asociado al item')
    activo = models.BooleanField(default=True)
    base = models.BooleanField(default=False, help_text='Indica si el item sera usado como base de porcentajes',
                               blank=True)
    requerido = models.BooleanField(default=False, help_text='Indica si el item es requerido')
    iva_ri = models.DecimalField(choices=ALIC_IVA, max_digits=4, decimal_places=2,
                                 verbose_name='IVA Responsable Inscripto', help_text='IVA Responsable Inscripto')
    iva_monotributo = models.DecimalField(choices=ALIC_IVA, max_digits=4, decimal_places=2,
                                          verbose_name='IVA Monotributo', help_text='IVA Monotributo')
    iva_consfinal = models.DecimalField(choices=ALIC_IVA, max_digits=4, decimal_places=2,
                                        verbose_name='IVA Consumidor Final', help_text='IVA Consumidor Final')
    iva_sujnocat = models.DecimalField(choices=ALIC_IVA, max_digits=4, decimal_places=2,
                                       verbose_name='IVA Sujeto no categorizado',
                                       help_text='IVA Sujeto no categorizado')
    iva_exento = models.DecimalField(choices=ALIC_IVA, max_digits=4, decimal_places=2, verbose_name='IVA Exento',
                                     help_text='IVA Exento')
    iva_nograv = models.DecimalField(choices=ALIC_IVA, max_digits=4, decimal_places=2, verbose_name='IVA No Gravado',
                                     help_text='IVA No gravado')

    def __unicode__(self):
        return self.nombre

    @property
    def tipo_display(self):
        return self.get_tipo_display()

    @property
    def aplicacion_display(self):
        return self.get_aplicacion_display()

    @property
    def servicio_display(self):
        return self.get_servicios_display()


class AsociacionItemAgrupacion(models.Model):
    # IVA_CHOICES = (('IVA21', 'IVA 21%'),
    #                ('IVA27', 'IVA 27%'),
    #                ('NOGRA', 'No Gravado'),
    #                ('EXENT', 'Exento'))

    agrupacion = models.ForeignKey(AgrupacionDeItems, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    # iva = models.CharField(max_length=5, choices=IVA_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)


class Escalones(models.Model):
    asociacion = models.ForeignKey(AsociacionItemAgrupacion, help_text="Asociacion a la que se aplicara el escalon.")
    item = models.ForeignKey(Items)
    desde = models.IntegerField(help_text="Valor base del escalon.")
    hasta = models.IntegerField(help_text="Valor final del escalon.")
    valor = models.FloatField(help_text="Costo en pesos de los intervalos ingresados en el escalon.")

    def __unicode__(self):
        return '%s - %s a %s' % (self.item, self.desde, self.hasta)


class Cesp(models.Model):
    nroCesp = models.CharField(unique=True, max_length=50, help_text="Número de CESP.")
    fecha = models.DateField(help_text="Fecha de validez del número CESP ingresado.")

    def __unicode__(self):
        return self.nroCesp


class CuotaCargoFijo(models.Model):
    fecha_generacion = models.DateField(auto_now_add=True)
    terreno = models.ForeignKey(Terreno)
    # items = models.ManyToManyField(Items, through='Cuota_items')
    items = models.ManyToManyField(Items)
    consumo_agua = models.IntegerField()
    cobrada = models.BooleanField(editable=False)
    factura_energia = models.ForeignKey('Factura', null=True, blank=True)


# class Cuota_items(models.Model):
#     cuota = models.ForeignKey(CuotaCargoFijo)
#     item = models.ForeignKey(Items)


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


class LecturasAgua(models.Model):
    fecha = models.DateField(auto_now_add=True)
    mes = models.IntegerField()
    ano = models.IntegerField()
    terreno = models.ForeignKey(Terreno)
    medidorAgua = models.CharField(max_length=30)
    lectura = models.IntegerField()
