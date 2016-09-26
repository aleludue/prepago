import json
import re
from StringIO import StringIO

from datetime import date

from decimal import Decimal

from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from prepapp.models import Socio, Terreno, Items, Cesp, Tarifa


def get_socios_fk(request):
    phrase = request.GET['ph']
    qs = []
    for fk in Socio.fk_fields:
        qs.append(Q(**{fk + '__icontains': phrase}))
    socios_qs = Socio.objects.filter(reduce(lambda x, y: x | y, qs))
    socios = []
    for socio in socios_qs:
        socios.append({'fk_display': socio.fk_display, 'pk': socio.pk})
    s = StringIO()
    json.dump(socios, s)
    s.seek(0)
    return HttpResponse(s.read())


def get_items_fijos_fk(request):
    phrase = request.GET['ph']
    items_qs = Items.objects.filter(nombre__icontains=phrase, aplicacion='CF', requerido=False)
    items = []
    for item in items_qs:
        items.append({'fk_display': item.nombre, 'pk': item.pk})
    s = StringIO()
    json.dump(items, s)
    s.seek(0)
    return HttpResponse(s.read())


def get_items_energia_fk(request):
    phrase = request.GET['ph']
    items_qs = Items.objects.filter(nombre__icontains=phrase, aplicacion='EN', requerido=False)
    items = []
    for item in items_qs:
        items.append({'fk_display': item.nombre, 'pk': item.pk})
    s = StringIO()
    json.dump(items, s)
    s.seek(0)
    return HttpResponse(s.read())


def get_items_fijos_req(request):
    items_qs = Items.objects.filter(aplicacion='CF', requerido=True)
    items = []
    for item in items_qs:
        items.append({'nombre': item.nombre, 'pk': item.pk})
    s = StringIO()
    json.dump(items, s)
    s.seek(0)
    return HttpResponse(s.read())


def get_items_energia_req(request):
    items_qs = Items.objects.filter(aplicacion='EN', requerido=True)
    items = []
    for item in items_qs:
        items.append({'nombre': item.nombre, 'pk': item.pk})
    s = StringIO()
    json.dump(items, s)
    s.seek(0)
    return HttpResponse(s.read())


def _getattr_foreingkey(obj, attr):
    pt = attr.count('.')
    if pt == 0:  # No hay clave foranea
        if attr.endswith('()'):
            re = getattr(obj, attr[:-2])()
        else:
            re = getattr(obj, attr)
        if isinstance(re, date):
            return re.strftime("%d/%m/%Y")
        if isinstance(re, Decimal):
            return "%.2f" % re
        else:
            return re
    else:
        nobj = getattr(obj, attr[:attr.find('.')])
        nattr = attr[attr.find('.') + 1:]
        return _getattr_foreingkey(nobj, nattr)


def filtering(get, dataset, data_struct, global_search):
    """
    :param get: Diccionario GET del request de la vista, para buscar los parametros
    :param dataset: Dataset con la info, normalmente objects.all()
    :param data_struct: Dictionario con la estructura de la tabla {0:'columna_a',1:'columna_b'}
    :param global_search: En que columna debe buscar el termino global
    :return: Dataset filtrado segun los parametros
    """
    # Extraccion de las busquedas indivuales
    individual_searchs_i = {}
    for item in get:
        match = re.match(r'columns\[(\d+)\]\[search\]\[value\]', item)
        if match and get[item]:
            individual_searchs_i[int(match.group(1))] = int(get[item])
    # Filtrado de los datos
    search = get['search[value]']
    queries_g = []
    for item in global_search:
        queries_g.append(Q(**{item + '__icontains': search}))
    qs = reduce(lambda x, y: x | y, queries_g)
    queries_i = []
    for k, v in individual_searchs_i.iteritems():
        if v == 'false':
            queries_i.append(Q(**{data_struct[k]: False}))
        if v == 'true':
            queries_i.append(Q(**{data_struct[k]: True}))
        else:
            queries_i.append(Q(**{data_struct[k] + '__icontains': v}))
    if individual_searchs_i:
        qi = reduce(lambda x, y: x & y, queries_i)
        qs = qs | qi
    return dataset.filter(qs)


def ordering(get, dataset, data_struct):
    individual_orders = {}
    for item in get:
        match_dir = re.match(r'order\[(\d+)\]\[dir\]', item)
        match_col = re.match(r'order\[(\d+)\]\[column\]', item)
        if match_dir or match_col and get[item]:
            if match_dir:
                i = int(match_dir.group(1))
                if i not in individual_orders:
                    individual_orders[i] = ['', '']
                individual_orders[i][0] = get[item]
            if match_col:
                i = int(match_col.group(1))
                if i not in individual_orders:
                    individual_orders[i] = ['', '']
                individual_orders[i][1] = get[item]
    dirs = {'asc': '', 'desc': '-'}
    ordering = []
    for k, order in individual_orders.iteritems():
        ordering.append(dirs[order[0]] + data_struct[int(order[1])])
    ordering = tuple(ordering)
    return dataset.order_by(*ordering)


def make_data(dataset, list_display, url_modif=None, url_suspen=None, url_hab=None, detalle=None):
    """
    :param dataset: Dataset con la info, normalmente objects.all()
    :param list_display:
    :return: Datos en Array
    """
    data = []
    for obj in dataset:
        row = map(lambda field: _getattr_foreingkey(obj, field), list_display)
        if url_modif:
            row.append(
                '<a class="mdl-button mdl-js-button mdl-button--icon mdl-button--colored" href="%s"><i class="material-icons">mode_edit</i></a>' % reverse(
                    url_modif, args=[obj.pk]))
        if url_suspen and url_hab:
            if not obj.activo:
                row.append(
                    '<a class="mdl-button mdl-js-button mdl-button--icon mdl-button--colored" href="%s"><i class="material-icons">keyboard_arrow_up</i></a>' % reverse(
                        url_hab,
                        args=[obj.pk]))
            else:
                row.append(
                    '<a class="mdl-button mdl-js-button mdl-button--icon mdl-button--colored" href="%s"><i class="material-icons">keyboard_arrow_down</i></a>' % reverse(
                        url_suspen,
                        args=[
                            obj.pk]))
        if detalle:
            real_detail = {}
            for field in re.findall(r'%\((\w+\(*\)*)\)s', detalle):
                real_detail[field] = getattr(obj, field[:-2])() if field.endswith("()") else getattr(obj, field)
            deta = detalle % real_detail
            row.insert(0, deta)
        data.append(row)
    return data


def get_socios_table(request):
    # SETEOS INICIALES
    objects = Socio.objects.all()
    list_display = ['nroSocio', 'razonSocial', 'domicilio', 'localidad', 'telefono']
    list_global_search = list_display
    data_struct = {0: 'nroSocio', 1: 'razonSocial', 2: 'domicilio', 3: 'localidad', 4: 'telefono'}

    # Cuenta total de articulos:
    recordsTotal = objects.count()

    # Filtrado de los bancos
    objects = filtering(request.GET, objects, data_struct, list_global_search)

    # Ordenado
    objects = ordering(request.GET, objects, data_struct)

    # Conteo de articulos despues dle filtrado
    recordsFiltered = objects.count()

    # finally, slice according to length sent by dataTables:
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    objects = objects[start: (start + length)]

    # extract information
    data = make_data(objects, list_display, "SociosModificar", "SociosSuspender", "SociosHabilitar")
    # define response
    response = {
        'data': data,
        'recordsTotal': recordsTotal,
        'recordsFiltered': recordsFiltered,
        'draw': request.GET['draw']
    }

    # serialize to json
    s = StringIO()
    json.dump(response, s)
    s.seek(0)
    return HttpResponse(s.read())


def get_terrenos_table(request):
    # SETEOS INICIALES
    objects = Terreno.objects.all()
    list_display = ['nroTerreno', 'socio__nroSocio', 'socio__razonSocial', 'domicilio', 'tarifa']
    list_global_search = list_display[0:2]
    data_struct = {0: 'nroTerreno', 1: 'socio__nroSocio', 2: 'socio__razonSocial', 3: 'domicilio', 4: 'tarifa'}

    # Cuenta total de articulos:
    recordsTotal = objects.count()

    # Filtrado de los bancos
    objects = filtering(request.GET, objects, data_struct, list_global_search)

    # Ordenado
    objects = ordering(request.GET, objects, data_struct)

    # Conteo de articulos despues dle filtrado
    recordsFiltered = objects.count()

    # finally, slice according to length sent by dataTables:
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    objects = objects[start: (start + length)]

    # extract information
    data = make_data(objects, list_display, "TerrenosModificar", "TerrenosSuspender", "TerrenosHabilitar")
    # define response
    response = {
        'data': data,
        'recordsTotal': recordsTotal,
        'recordsFiltered': recordsFiltered,
        'draw': request.GET['draw']
    }

    # serialize to json
    s = StringIO()
    json.dump(response, s)
    s.seek(0)
    return HttpResponse(s.read())


def get_items_table(request):
    # SETEOS INICIALES
    objects = Items.objects.all()
    list_display = ['nombre', 'tipo_display', 'aplicacion_display']
    list_global_search = ['nombre']
    data_struct = {0: 'nombre', 1: 'tipo', 2: 'aplicacion'}

    # Cuenta total de articulos:
    recordsTotal = objects.count()

    # Filtrado de los bancos
    objects = filtering(request.GET, objects, data_struct, list_global_search)

    # Ordenado
    objects = ordering(request.GET, objects, data_struct)

    # Conteo de articulos despues dle filtrado
    recordsFiltered = objects.count()

    # finally, slice according to length sent by dataTables:
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    objects = objects[start: (start + length)]

    # extract information
    data = make_data(objects, list_display, "ItemsModificar", "ItemsSuspender", "ItemsHabilitar")
    # define response
    response = {
        'data': data,
        'recordsTotal': recordsTotal,
        'recordsFiltered': recordsFiltered,
        'draw': request.GET['draw']
    }

    # serialize to json
    s = StringIO()
    json.dump(response, s)
    s.seek(0)
    return HttpResponse(s.read())


def get_cesp_table(request):
    # SETEOS INICIALES
    objects = Cesp.objects.all()
    list_display = ['nroCesp', 'fecha']
    list_global_search = list_display
    data_struct = {0: 'nroCesp', 1: 'fecha'}

    # Cuenta total de articulos:
    recordsTotal = objects.count()

    # Filtrado de los bancos
    objects = filtering(request.GET, objects, data_struct, list_global_search)

    # Ordenado
    objects = ordering(request.GET, objects, data_struct)

    # Conteo de articulos despues dle filtrado
    recordsFiltered = objects.count()

    # finally, slice according to length sent by dataTables:
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    objects = objects[start: (start + length)]

    # extract information
    data = make_data(objects, list_display, "CespModificar")
    # define response
    response = {
        'data': data,
        'recordsTotal': recordsTotal,
        'recordsFiltered': recordsFiltered,
        'draw': request.GET['draw']
    }

    # serialize to json
    s = StringIO()
    json.dump(response, s)
    s.seek(0)
    return HttpResponse(s.read())


def get_tarifas_table(request):
    # SETEOS INICIALES
    objects = Tarifa.objects.all()
    list_display = ['nombre']
    list_global_search = list_display
    data_struct = {0: 'nombre'}

    # Cuenta total de articulos:
    recordsTotal = objects.count()

    # Filtrado de los bancos
    objects = filtering(request.GET, objects, data_struct, list_global_search)

    # Ordenado
    objects = ordering(request.GET, objects, data_struct)

    # Conteo de articulos despues dle filtrado
    recordsFiltered = objects.count()

    # finally, slice according to length sent by dataTables:
    start = int(request.GET['start'])
    length = int(request.GET['length'])
    objects = objects[start: (start + length)]

    url_modif = None

    data = []
    for obj in objects:
        row = map(lambda field: _getattr_foreingkey(obj, field), list_display)
        html = "<ul>"
        for agrup in obj.agrupaciondeitems_set.all():
            html += "<li>Escala " + str(agrup.desde) + " a " + str(agrup.hasta) + "<ul><li>Cargos Fijos<ul>"
            for asoc in agrup.asociacionitemagrupacion_set.filter(item__aplicacion='CF'):
                html += "<li>" + asoc.item.nombre + " - " + asoc.item.get_tipo_display() + " - $" + str(asoc.valor) + "</li>"
            html += "</ul></li><li>Energia<ul>"
            for asoc in agrup.asociacionitemagrupacion_set.filter(item__aplicacion='EN'):
                if asoc.item.tipo == "ESC":
                    html += "<li>" + asoc.item.nombre + " - " + asoc.item.get_tipo_display() + "<ul>"
                    for esc in asoc.escalones_set.all():
                        html += "<li>" + str(esc.desde) + " a " + str(esc.hasta) + " - $" + str(esc.valor) + "</li>"
                    html += "</ul> "
                else:
                    html += "<li>" + asoc.item.nombre + " - " + asoc.item.get_tipo_display() + " - $" + str(asoc.valor) + "</li></ul>"
            html += "</ul></li>"
        html += "</ul>"

        row.append(html)
        if url_modif:
            row.append(
                '<a class="mdl-button mdl-js-button mdl-button--icon mdl-button--colored" href="%s"><i class="material-icons">mode_edit</i></a>' % reverse(
                    url_modif, args=[obj.pk]))
        data.append(row)

    # define response
    response = {
        'data': data,
        'recordsTotal': recordsTotal,
        'recordsFiltered': recordsFiltered,
        'draw': request.GET['draw']
    }

    # serialize to json
    s = StringIO()
    json.dump(response, s)
    s.seek(0)
    return HttpResponse(s.read())
