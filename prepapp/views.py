import json
import re

from django.core.urlresolvers import reverse_lazy
from django.forms.formsets import formset_factory
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template.context import RequestContext
from django.template.context_processors import csrf
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView

from prepapp.forms import SociosForm, TerrenosForm, TarifaForm, CespForm, EscalasForm, ItemsFijoForm, ItemsEnergiaForm, \
    ItemsForm, ImportacionAguaForm
from prepapp.models import Socio, Terreno, Tarifa, Escalones, Cesp, Items, AgrupacionDeItems, AsociacionItemAgrupacion, \
    LecturasAgua


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


def tarifaConfiguracion(request):
    if request.method == 'POST':  # If the form has been submitted...
        tarifaForm = TarifaForm(request.POST)
        EscalaFormset = formset_factory(EscalasForm, extra=0)
        escalaFormset = EscalaFormset(request.POST, prefix='escala')
        formsets_fijos = formsets_energia = []
        all_formsets_valid = True
        for i, escala in enumerate(escalaFormset.forms):
            ItemFijoFormset = formset_factory(ItemsFijoForm, extra=0)
            itemFijoFormset = ItemFijoFormset(request.POST, prefix='fijos-' + str(i))
            all_formsets_valid = all_formsets_valid and itemFijoFormset.is_valid()
            formsets_fijos.append(itemFijoFormset)
            ItemEnergiaFormset = formset_factory(ItemsEnergiaForm, extra=0)
            itemEnergiaFormset = ItemEnergiaFormset(request.POST, prefix='energia-' + str(i))
            all_formsets_valid = all_formsets_valid and itemEnergiaFormset.is_valid()
            formsets_energia.append(itemEnergiaFormset)
        if tarifaForm.is_valid() and escalaFormset.is_valid() and all_formsets_valid:
            tarifa = tarifaForm.save()
            EscalaFormset = formset_factory(EscalasForm, extra=0)
            escalaFormset = EscalaFormset(request.POST, prefix='escala')
            for i, form in enumerate(escalaFormset.forms):
                escala = AgrupacionDeItems(tarifa=tarifa,
                                           desde=form.cleaned_data['desde'],
                                           hasta=form.cleaned_data['hasta'])
                escala.save()
                ItemFijoFormset = formset_factory(ItemsFijoForm, extra=0)
                itemFijoFormset = ItemFijoFormset(request.POST, prefix='fijos-' + str(i))
                for form in itemFijoFormset.forms:
                    if form.cleaned_data['item'].tipo == "ESC":  # Item escalonado--0:40=1.33;41:80=1.34
                        escalones = form.cleaned_data['valor'].split(";")
                        asoc = AsociacionItemAgrupacion(agrupacion=escala,
                                                        item=form.cleaned_data['item'],
                                                        valor=None)
                        asoc.save()
                        for escalon in escalones:
                            regex = re.search("(\d+):(\d+)=(.+)", escalon)
                            Escalones(asociacion=asoc,
                                      item=form.cleaned_data['item'],
                                      desde=regex.group(1),
                                      hasta=regex.group(2),
                                      valor=regex.group(3)).save()
                    else:
                        AsociacionItemAgrupacion(agrupacion=escala,
                                                 item=form.cleaned_data['item'],
                                                 valor=form.cleaned_data['valor']).save()
                ItemEnergiaFormset = formset_factory(ItemsEnergiaForm, extra=0)
                itemEnergiaFormset = ItemEnergiaFormset(request.POST, prefix='energia-' + str(i))
                for form in itemEnergiaFormset.forms:
                    if form.cleaned_data['item'].tipo == "ESC":  # Item escalonado--0:40=1.33;41:80=1.34
                        escalones = form.cleaned_data['valor'].split(";")
                        asoc = AsociacionItemAgrupacion(agrupacion=escala,
                                                        item=form.cleaned_data['item'],
                                                        valor=None)
                        asoc.save()
                        for escalon in escalones:
                            regex = re.search("(\d+):(\d+)=(.+)", escalon)
                            Escalones(asociacion=asoc,
                                      item=form.cleaned_data['item'],
                                      desde=regex.group(1),
                                      hasta=regex.group(2),
                                      valor=regex.group(3)).save()
                    else:
                        AsociacionItemAgrupacion(agrupacion=escala,
                                                 item=form.cleaned_data['item'],
                                                 valor=form.cleaned_data['valor']).save()

            return HttpResponseRedirect(reverse_lazy('TarifasList'))

    else:
        tarifaForm = TarifaForm()
        EscalasFormset = formset_factory(EscalasForm, extra=1)
        escalasFormset = EscalasFormset(prefix='escala')
        ItemsFijos = formset_factory(ItemsFijoForm, extra=0)
        formsets_fijos = []
        req_fijos = Items.objects.filter(requerido=True, aplicacion='CF')
        initial_req_fijos = [{'item': req} for req in req_fijos]
        itemsFijos = ItemsFijos(prefix='fijos-0', initial=initial_req_fijos)
        formsets_fijos.append(itemsFijos)
        ItemsEnergia = formset_factory(ItemsEnergiaForm, extra=0)
        formsets_energia = []
        req_energia = Items.objects.filter(requerido=True, aplicacion='EN')
        initial_req_energia = [{'item': req} for req in req_energia]
        itemsEnergia = ItemsEnergia(prefix='energia-0', initial=initial_req_energia)
        formsets_energia.append(itemsEnergia)

    c = {'tarifaForm': tarifaForm,
         'escalasFormset': escalasFormset,
         'formsets_energia': formsets_energia,
         'formsets_fijos': formsets_fijos,
         }
    c.update(csrf(request))

    return render_to_response('tarifas/tarifas_form.html', c)


def tarifaEdicion(request, pk):
    if request.method == 'POST':  # If the form has been submitted...
        tarifaForm = TarifaForm(request.POST, instance=Tarifa.objects.get(pk=pk))
        EscalaFormset = formset_factory(EscalasForm, extra=0)
        escalaFormset = EscalaFormset(request.POST, prefix='escala')
        formsets_fijos = formsets_energia = []
        all_formsets_valid = True
        for i, escala in enumerate(escalaFormset.forms):
            ItemFijoFormset = formset_factory(ItemsFijoForm, extra=0)
            itemFijoFormset = ItemFijoFormset(request.POST, prefix='fijos-' + str(i))
            all_formsets_valid = all_formsets_valid and itemFijoFormset.is_valid()
            formsets_fijos.append(itemFijoFormset)
            ItemEnergiaFormset = formset_factory(ItemsEnergiaForm, extra=0)
            itemEnergiaFormset = ItemEnergiaFormset(request.POST, prefix='energia-' + str(i))
            all_formsets_valid = all_formsets_valid and itemEnergiaFormset.is_valid()
            formsets_energia.append(itemEnergiaFormset)
        if tarifaForm.is_valid() and escalaFormset.is_valid() and all_formsets_valid:
            tarifa = tarifaForm.save()
            for form in escalaFormset.forms:
                if form.cleaned_data['escala']:
                    agrup = form.cleaned_data['escala']
                    agrup.desde = form.cleaned_data['desde']
                    agrup.hasta = form.cleaned_data['hasta']
                    agrup.save()
                else:
                    escala = AgrupacionDeItems(tarifa=tarifa,
                                               desde=form.cleaned_data['desde'],
                                               hasta=form.cleaned_data['hasta'])
                    escala.save()
                for form in itemFijoFormset.forms:
                    if form.cleaned_data['asoc']:
                        asoc = form.cleaned_data['asoc']
                        asoc.item = form.cleaned_data['item']
                        if form.cleaned_data['item'].tipo == "ESC":  # Item escalonado--0:40=1.33;41:80=1.34
                            asoc.escalones_set.all().delete()  # Borro todos los escalones
                            escalones = form.cleaned_data['valor'].split(";")
                            for escalon in escalones:
                                regex = re.search("(\d+):(\d+)=(.+)", escalon)
                                Escalones(asociacion=asoc,
                                          desde=regex.group(1),
                                          hasta=regex.group(2),
                                          valor=regex.group(3)).save()
                        else:
                            asoc.valor = form.cleaned_data['valor']
                        asoc.save()
                    else:  # Asociacion nueva
                        if form.cleaned_data['item'].tipo == "ESC":  # Item escalonado--0:40=1.33;41:80=1.34
                            escalones = form.cleaned_data['valor'].split(";")
                            asoc = AsociacionItemAgrupacion(agrupacion=escala,
                                                            item=form.cleaned_data['item'],
                                                            valor=None)
                            asoc.save()
                            for escalon in escalones:
                                regex = re.search("(\d+):(\d+)=(.+)", escalon)
                                Escalones(asociacion=asoc,
                                          desde=regex.group(1),
                                          hasta=regex.group(2),
                                          valor=regex.group(3)).save()
                        else:
                            AsociacionItemAgrupacion(agrupacion=escala,
                                                     item=form.cleaned_data['item'],
                                                     valor=form.cleaned_data['valor']).save()
                for form in itemEnergiaFormset.forms:
                    if form.cleaned_data['asoc']:
                        asoc = form.cleaned_data['asoc']
                        asoc.item = form.cleaned_data['item']
                        if form.cleaned_data['item'].tipo == "ESC":  # Item escalonado--0:40=1.33;41:80=1.34
                            asoc.escalones_set.all().delete()  # Borro todos los escalones
                            escalones = form.cleaned_data['valor'].split(";")
                            for escalon in escalones:
                                regex = re.search("(\d+):(\d+)=(.+)", escalon)
                                Escalones(asociacion=asoc,
                                          desde=regex.group(1),
                                          hasta=regex.group(2),
                                          valor=regex.group(3)).save()
                        else:
                            asoc.valor = form.cleaned_data['valor']
                        asoc.save()
                    else:  # Asociacion nueva
                        if form.cleaned_data['item'].tipo == "ESC":  # Item escalonado--0:40=1.33;41:80=1.34
                            escalones = form.cleaned_data['valor'].split(";")
                            asoc = AsociacionItemAgrupacion(agrupacion=escala,
                                                            item=form.cleaned_data['item'],
                                                            valor=None)
                            asoc.save()
                            for escalon in escalones:
                                regex = re.search("(\d+):(\d+)=(.+)", escalon)
                                Escalones(asociacion=asoc,
                                          desde=regex.group(1),
                                          hasta=regex.group(2),
                                          valor=regex.group(3)).save()
                        else:
                            AsociacionItemAgrupacion(agrupacion=escala,
                                                     item=form.cleaned_data['item'],
                                                     valor=form.cleaned_data['valor']).save()
            return HttpResponseRedirect(reverse_lazy('TarifasList'))

    else:
        tarifa = Tarifa.objects.get(pk=pk)
        tarifaForm = TarifaForm(instance=tarifa)
        EscalasFormset = formset_factory(EscalasForm, extra=0)
        initial_escala = [{'escala': escala, 'desde': escala.desde, 'hasta': escala.hasta} for escala in
                          tarifa.agrupaciondeitems_set.all()]
        escalasFormset = EscalasFormset(prefix='escala', initial=initial_escala)
        ItemsFijos = formset_factory(ItemsFijoForm, extra=0)
        formsets_fijos = []
        for idx, escala in enumerate(tarifa.agrupaciondeitems_set.all()):
            initial_fijos = [{'item': cf.item, 'valor': cf.valor_escalonado()} for cf in
                             escala.asociacionitemagrupacion_set.filter(item__aplicacion='CF')]
            itemsFijos = ItemsFijos(prefix='fijos-' + str(idx), initial=initial_fijos)
            formsets_fijos.append(itemsFijos)
        ItemsEnergia = formset_factory(ItemsEnergiaForm, extra=0)
        formsets_energia = []
        for idx, escala in enumerate(tarifa.agrupaciondeitems_set.all()):
            initial_energia = [{'item': cf.item, 'valor': cf.valor_escalonado()} for cf in
                               escala.asociacionitemagrupacion_set.filter(item__aplicacion='EN')]
            itemsEnergia = ItemsEnergia(prefix='energia-' + str(idx), initial=initial_energia)
            formsets_energia.append(itemsEnergia)

    c = {'tarifaForm': tarifaForm,
         'escalasFormset': escalasFormset,
         'formsets_energia': formsets_energia,
         'formsets_fijos': formsets_fijos,
         }
    c.update(csrf(request))

    return render_to_response('tarifas/tarifas_form_update.html', c)


class ItemsAlta(CreateView):
    template_name = "items/items_form.html"
    model = Items
    form_class = ItemsForm


class ItemsList(TemplateView):
    template_name = "items/items_list.html"


class ItemsAlta(CreateView):
    template_name = "items/items_form.html"
    model = Items
    form_class = ItemsForm
    success_url = reverse_lazy('ItemsList')


class ItemsModificar(UpdateView):
    template_name = "items/items_form.html"
    model = Items
    form_class = ItemsForm
    success_url = reverse_lazy('ItemsList')


def itemsSuspender(request, pk):
    item = Items.objects.get(pk=pk)
    item.activo = False
    item.save()
    return HttpResponseRedirect(reverse_lazy('ItemsList'))


def itemsHabilitar(request, pk):
    item = Items.objects.get(pk=pk)
    item.activo = True
    item.save()
    return HttpResponseRedirect(reverse_lazy('ItemsList'))


class CespList(TemplateView):
    template_name = "cesp/cesp_list.html"


class CespAlta(CreateView):
    template_name = "cesp/cesp_form.html"
    model = Cesp
    form_class = CespForm
    success_url = reverse_lazy('CespList')


class CespModificar(UpdateView):
    template_name = "cesp/cesp_form.html"
    model = Cesp
    form_class = CespForm
    success_url = reverse_lazy('CespList')


class ImportacionAgua(View):
    def get(self, request):
        c = RequestContext(request)
        c.update({'form': ImportacionAguaForm()})
        return render_to_response("importacion/importacion_form.html", c)

    def post(self, request):
        form = ImportacionAguaForm(request.POST, request.FILES)
        if form.is_valid():
            lecturas = {}
            for file in form.cleaned_data['agua']:
                for line in file:
                    try:
                        lecturas[int(line[80:89])] = int(line[161:167])
                    except ValueError as e:
                        print e.message
                terrenos_sin_lecturas = []
                terrenos = Terreno.objects.filter(activo=True)
                exito = 0
                for terreno in terrenos:
                    try:
                        lectura = lecturas[terreno.nroMedidorAgua]
                        LecturasAgua(mes=form.cleaned_data['mes'],
                                     ano=form.cleaned_data['ano'],
                                     terreno=terreno,
                                     medidorAgua=terreno.nroMedidorAgua,
                                     lectura=lectura).save()
                        exito += 1
                    except IndexError:
                        terrenos_sin_lecturas.append(terreno)
                        pass
            c = {'terrenos_sin_lecturas': terrenos_sin_lecturas,
                 'lecturas_exitosas': exito}
            return render_to_response("importacion/importacion_terminada.html", c)
        c = {'form': form}
        return render(request, "importacion/importacion_terminada.html", c)
