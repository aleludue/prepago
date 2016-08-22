from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from prepapp.forms import SociosForm
from prepapp.models import Socio, Terreno, Tarifa, EscalonesEnergia


class SociosList(TemplateView):
    template_name = "socios/socios_list.html"

class SociosAlta(CreateView):
    template_name = "socios/socios_form.html"
    form_class = SociosForm
    model = Socio

class SociosModificar(UpdateView):
    template_name = "socios/socios_form.html"
    model = Socio
    fields = ['nroSocio', 'razonSocial', 'domicilio', 'telefono', 'localidad']


class TerrenoAlta(CreateView):
    template_name = "terrenos/terrenos_form.html"
    model = Terreno
    fields = ['socio', 'nroTerreno', 'domicilio', 'condicionIva', 'nroMedidorEnergia', 'cargoConsumoAgua', 'tarifa']

class TerrenoModificar(UpdateView):
    template_name = "terrenos/terrenos_form.html"
    model = Terreno
    fields = ['socio', 'nroTerreno', 'domicilio', 'condicionIva', 'nroMedidorEnergia', 'cargoConsumoAgua', 'tarifa']

class TarifaAlta(CreateView):
    template_name = "tarifas/tarifas_form.html"
    model = Tarifa
    fields = ['nombre']

class TarifaModificar(UpdateView):
    template_name = "tarifas/tarifas_form.html"
    model = Tarifa
    fields = ['nombre']

class EscalonesEnergiaAlta(CreateView):
    template_name = "escalonesenergia/escalonesenergia_form.html"
    model = EscalonesEnergia
    fields = ['tarifa', 'desde', 'hasta', 'valor']

class EscalonesEnergiaModificar(UpdateView):
    template_name = "escalonesenergia/escalonesenergia_form.html"
    model = EscalonesEnergia
    fields = ['tarifa', 'desde', 'hasta', 'valor']