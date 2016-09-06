from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from prepapp.forms import SociosForm, TerrenosForm, TarifasForm, EscalonesEnergiaForm, ItemsForm, CespForm
from prepapp.models import Socio, Terreno, Tarifa, EscalonesEnergia, Cesp, Items


class SociosList(TemplateView):
    template_name = "socios/socios_list.html"


class SociosAlta(CreateView):
    success_url = reverse_lazy("SociosList")
    template_name = "socios/socios_form.html"
    form_class = SociosForm
    model = Socio


class SociosModificar(UpdateView):
    success_url = reverse_lazy('SociosList')
    template_name = "socios/socios_form.html"
    form_class = SociosForm
    model = Socio


def sociosSuspender(request, pk):
    socio = Socio.objects.get(pk=pk)
    socio.activo = False
    socio.save()
    return HttpResponseRedirect(reverse_lazy('SociosList'))


def sociosHabilitar(request, pk):
    socio = Socio.objects.get(pk=pk)
    socio.activo = True
    socio.save()
    return HttpResponseRedirect(reverse_lazy('SociosList'))


class TerrenoList(TemplateView):
    template_name = "terrenos/terrenos_list.html"

class TerrenoAlta(CreateView):
    success_url = reverse_lazy("TerrenosList")
    template_name = "terrenos/terrenos_form.html"
    model = Terreno
    form_class = TerrenosForm

class TerrenoModificar(UpdateView):
    success_url = reverse_lazy('TerrenoList')
    template_name = "terrenos/terrenos_form.html"
    model = Terreno
    form_class = TerrenosForm

def terrenosSuspender(request, pk):
    terreno = Terreno.objects.get(pk=pk)
    terreno.activo = False
    terreno.save()
    return HttpResponseRedirect(reverse_lazy('TerrenosList'))


def terrenosHabilitar(request, pk):
    terreno = Terreno.objects.get(pk=pk)
    terreno.activo = True
    terreno.save()
    return HttpResponseRedirect(reverse_lazy('TerrenosList'))


class TarifaList(TemplateView):
    template_name = "tarifas/tarifas_list.html"

class TarifaAlta(CreateView):
    template_name = "tarifas/tarifas_form.html"
    model = Tarifa
    form_class = TarifasForm

class TarifaModificar(UpdateView):
    template_name = "tarifas/tarifas_form.html"
    model = Tarifa
    form_class = TarifasForm
    success_url = reverse_lazy('TarifaList')

class EscalonesEnergiaList(TemplateView):
    template_name = "escalonesenergia/escalonesenergia_list.html"

class EscalonesEnergiaAlta(CreateView):
    template_name = "escalonesenergia/escalonesenergia_form.html"
    model = EscalonesEnergia
    form_class = EscalonesEnergiaForm

class EscalonesEnergiaModificar(UpdateView):
    template_name = "escalonesenergia/escalonesenergia_form.html"
    model = EscalonesEnergia
    form_class = EscalonesEnergiaForm
    success_url = reverse_lazy('EscalonesEnergiaList')

class ItemsAlta(CreateView):
    template_name = "items/items_form.html"
    model = Items
    form_class = ItemsForm

class ItemsModificar(UpdateView):
    template_name = "items/items_form.html"
    model = Items
    form_class = ItemsForm

class CespList(TemplateView):
    template_name = "cesp/cesp_list.html"

class CespAlta(CreateView):
    template_name = "cesp/cesp_form.html"
    model = Cesp
    form_class = CespForm

class CespModificar(UpdateView):
    template_name = "cesp/cesp_form.html"
    model = Cesp
    form_class = CespForm
    success_url = reverse_lazy('CespList')



