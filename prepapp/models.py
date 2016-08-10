from __future__ import unicode_literals

from django.db import models


# Create your models here.
from django.utils import timezone


class Socio(models.Model):
    LOCALIDAD_CHOICES = ((1, 'Brinkmann'),
                         (2, 'Seeber'),
                         (3, 'Col. Vignaud'))

    nroSocio = models.IntegerField(primary_key=True)
    razonSocial = models.CharField(max_length=140)
    domicilio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fechaCreacion = models.DateField(auto_now_add=True)
    localidad = models.IntegerField(choices=LOCALIDAD_CHOICES)
    activo = models.BooleanField(default=True)


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

class RecambioMedidor(models.Model):
    terreno = models.ForeignKey(Terreno)
    fecha = models.DateField(default=timezone.now())
    nroMedidor = models.CharField(max_length=30)
