from django.core.urlresolvers import reverse_lazy
from django.forms.formsets import formset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template.context_processors import csrf
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from prepapp.forms import SociosForm, TerrenosForm, TarifaForm, CespForm, EscalasForm, ItemsFijoForm, ItemsEnergiaForm, \
    ItemsForm
from prepapp.models import Socio, Terreno, Tarifa, Escalones, Cesp, Items


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
    print request.POST
    if request.method == 'POST':  # If the form has been submitted...
        # Paso todos los campos en POST de cantidad que esten en tiempo a decimal
        CPOST = request.POST.copy()
        for k, v in CPOST.iteritems():
            if "cantidad" in k and ":" in v:
                entero = int(CPOST[k].split(":")[0])
                decimal = float(CPOST[k].split(":")[1]) / 60
                decimal = Decimal("%.3f" % decimal)
                CPOST[k] = "%s" % (entero + decimal)

        facturaForm = VentaForm(CPOST)

        print facturaForm.is_valid()
        print facturaForm.errors

        #print articuloCompuestoFormset.is_valid()
        #print articuloCompuestoFormset.errors
        if facturaForm.is_valid():
            factura = facturaForm.save(commit=False)
            periodo = Periodo.objects.filter(mes=factura.fecha.month, ano=factura.fecha.year)[0]
            factura.periodo = periodo
            if factura.descuento is None:
                factura.descuento = 0
            if not ES_MONOTRIBUTO:
                if factura.cliente.cond_iva == "RI":
                    factura.tipo = facturaForm.cleaned_data['tipoDisplay'] + "A"
                else:
                    factura.tipo = facturaForm.cleaned_data['tipoDisplay'] + "B"
            else:
                factura.tipo = facturaForm.cleaned_data['tipoDisplay'] + "C"
            #FIN PROCESO EN FACTURA, FALTAN LOS TOTALES
            print factura.subtotal
            factura.neto = factura.subtotal - (factura.subtotal * factura.descuento / Decimal(100))
            factura.iva21 = 0 if factura.tipo.endswith('C') else factura.neto * Decimal("0.21")
            factura.iva105 = 0
            factura.total = factura.saldo = factura.neto + factura.iva21
            factura.save()
            detalleFormset = iNuevoDetalleFormset(CPOST, prefix='det_venta', instance=factura)
            print detalleFormset.is_valid()
            print detalleFormset.errors
            if detalleFormset.is_valid():
                subtotal = 0
                i = 0
                for form in detalleFormset.forms:
                    detalleItem = form.save(commit=False)
                    if detalleItem.descuento is None:
                        detalleItem.descuento = 0
                    if detalleItem.tipo_articulo == "AA":
                        detalleItem.articulo_personalizado = ""
                        detalleItem.linea_articulo_personalizado = None
                    else:
                        detalleItem.articulo = None
                    if factura.tipo.endswith('A') or factura.tipo.endswith('C'):
                        sub = detalleItem.cantidad * detalleItem.precio_unitario
                        subtotal += sub - (sub * detalleItem.descuento / Decimal(100))
                    elif factura.tipo.endswith('B'):
                        sub = detalleItem.cantidad * (detalleItem.precio_unitario / Decimal(1.21))
                        subtotal += sub - (sub * detalleItem.descuento / Decimal(100))
                        detalleItem.precio_unitario = detalleItem.precio_unitario / Decimal(1.21)
                    detalleItem.save()
                    if detalleItem.tipo_articulo == 'AC':
                        articuloCompuestoFormset = iNuevoArticuloCompuestoFormset(CPOST, prefix='art_comp-'+str(i), instance=detalleItem)
                        print articuloCompuestoFormset.is_valid()
                        print articuloCompuestoFormset.errors
                        if articuloCompuestoFormset.is_valid():
                            #factura.save()
                            #detalleItem.save()
                            for form in articuloCompuestoFormset.forms:
                                articuloCompuesto = form.save(commit=False)
                                # Si es factura B, quito el iva.
                                #articuloCompuesto.detalle_venta = dict_forms[int(id_deta)]
                                articuloCompuesto.precio_unitario = articuloCompuesto.precio_unitario / Decimal('1.21') if \
                                    articuloCompuesto.detalle_venta.venta.tipo[-1:] == 'B' else articuloCompuesto.precio_unitario
                                articuloCompuesto.descuento = detalleItem.descuento
                                articuloCompuesto.save()
                    i+=1

            if factura.tipo.startswith("FA") or factura.tipo.startswith("ND"):
                saldo_temp = factura.saldo
                if factura.cliente.saldo < 0:  # Esto significa que hay NC con saldos a descontar
                    otros_comp = Venta.objects.filter(Q(cliente=factura.cliente), Q(tipo__startswith="NC"),
                                                      ~Q(saldo=0)).order_by('fecha', 'numero')
                    if otros_comp:
                        for k, comp in otros_comp.iteritems():
                            if factura.saldo == 0:
                                break
                            if factura.saldo >= comp.saldo:
                                factura.saldo -= comp.saldo
                                comp.saldo = 0
                                comp.save()
                            else:
                                comp.saldo -= factura.saldo
                                factura.saldo = 0
                                comp.save()
                factura.cliente.saldo += saldo_temp
            if factura.tipo.startswith("NC"):
                saldo_temp = factura.saldo
                factura.pagado = True
                if factura.comprobante_relacionado.total - Decimal(
                        '0.009') < factura.total < factura.comprobante_relacionado.total + Decimal('0.009'):
                    factura.comprobante_relacionado.pagado = True
                    factura.comprobante_relacionado.save()
                # Resto de los saldos de otros comprobantes
                if factura.cliente.saldo > 0:  # Esto significa que hay FA o ND con saldos a descontar
                    otros_comp = Venta.objects.filter(Q(cliente=factura.cliente),
                                                      Q(tipo__startswith="FA") | Q(tipo__startswith="ND"),
                                                      ~Q(saldo=0)).order_by('fecha', 'numero')
                    if otros_comp:
                        for k, comp in otros_comp.iteritems():
                            if factura.saldo == 0:
                                break
                            if factura.saldo >= comp.saldo:
                                factura.saldo -= comp.saldo
                                comp.saldo = 0
                                comp.pagado = True
                                comp.save()
                            else:
                                comp.saldo -= factura.saldo
                                factura.saldo = 0
                                comp.save()
                factura.cliente.saldo -= saldo_temp
            factura.save()
            factura.cliente.save()
            # factura.comprobante_relacionado.save()
            #Guardo todos los detalles y articulos compuestos

            if not USA_FACTURA_ELECTRONICA:
                factura.aprobado = True
                factura.punto_venta = utils.get_pto_vta(factura)
                factura.numero = utils.get_num_comp(factura)
                factura.save()
            return HttpResponseRedirect(reverse_lazy('nuevaVenta'))

    else:
        tarifaForm = TarifaForm()
        EscalasFormset = formset_factory(EscalasForm, extra=1)
        escalasFormset = EscalasFormset(prefix='escala')
        ItemsFijos = formset_factory(ItemsFijoForm, extra=0)
        req_fijos = Items.objects.filter(requerido=True, aplicacion='CF')
        initial_req_fijos = [{'item': req} for req in req_fijos]
        print initial_req_fijos
        itemsFijos = ItemsFijos(prefix='fijos-0', initial=initial_req_fijos)
        ItemsEnergia = formset_factory(ItemsEnergiaForm, extra=0)
        req_energia = Items.objects.filter(requerido=True, aplicacion='EN')
        initial_req_energia = [{'item': req} for req in req_energia]
        print initial_req_energia
        itemsEnergia = ItemsEnergia(prefix='energia-0', initial=initial_req_energia)
        #detalleFormset = NuevoDetalleFormset(prefix='det_venta')
        #detalleFormset = iNuevoDetalleFormset(prefix='det_venta')
        #articuloCompuestoFormset = NuevoArticuloCompuestoFormset(prefix='art_comp')
        #articuloCompuestoFormset = iNuevoArticuloCompuestoFormset(prefix='art_comp-0')
    # For CSRF protection
    # See http://docs.djangoproject.com/en/dev/ref/contrib/csrf/
    # set_trace()
    c = {'tarifaForm': tarifaForm,
         'escalasFormset': escalasFormset,
         'itemsEnergia':itemsEnergia,
         'itemsFijos':itemsFijos,
         #'articuloCompuestoFormset': articuloCompuestoFormset,
         }
    c.update(csrf(request))

    return render_to_response('tarifas/tarifas_form.html', c)




class TarifaAlta(CreateView):
    template_name = "tarifas/tarifas_form.html"
    model = Tarifa
    form_class = TarifaForm

class TarifaModificar(UpdateView):
    template_name = "tarifas/tarifas_form.html"
    model = Tarifa
    form_class = TarifaForm
    success_url = reverse_lazy('TarifaList')

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



