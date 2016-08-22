from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from prepapp.forms import SociosForm, TerrenosForm, TarifasForm, EscalonesEnergiaForm, ItemsForm, CespForm
from prepapp.models import Socio, Terreno, Tarifa, EscalonesEnergia, Items, Cesp


class SociosList(TemplateView):
    template_name = "socios/socios_list.html"

class SociosAlta(CreateView):
    template_name = "socios/socios_form.html"
    model = Socio
    form_class = SociosForm

class SociosModificar(UpdateView):
    template_name = "socios/socios_form.html"
    model = Socio
    form_class = SociosForm

class TerrenoAlta(CreateView):
    template_name = "terrenos/terrenos_form.html"
    model = Terreno
    form_class = TerrenosForm

class TerrenoModificar(UpdateView):
    template_name = "terrenos/terrenos_form.html"
    model = Terreno
    form_class = TerrenosForm

class TarifaAlta(CreateView):
    template_name = "tarifas/tarifas_form.html"
    model = Tarifa
    form_class = TarifasForm

class TarifaModificar(UpdateView):
    template_name = "tarifas/tarifas_form.html"
    model = Tarifa
    form_class = TarifasForm

class EscalonesEnergiaAlta(CreateView):
    template_name = "escalonesenergia/escalonesenergia_form.html"
    model = EscalonesEnergia
    form_class = EscalonesEnergiaForm

class EscalonesEnergiaModificar(UpdateView):
    template_name = "escalonesenergia/escalonesenergia_form.html"
    model = EscalonesEnergia
    form_class = EscalonesEnergiaForm

class ItemsAlta(CreateView):
    template_name = "items/items_form.html"
    model = Items
    form_class = ItemsForm

class ItemsModificar(UpdateView):
    template_name = "items/items_form.html"
    model = Items
    form_class = ItemsForm

class CespAlta(CreateView):
    template_name = "cesp/cesp_form.html"
    model = Cesp
    form_class = CespForm

class CespModificar(UpdateView):
    template_name = "cesp/cesp_form.html"
    model = Cesp
    form_class = CespForm



