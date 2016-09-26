"""prepago URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from prepapp.api import get_socios_fk, get_socios_table, get_terrenos_table, get_items_table, get_cesp_table, \
    get_items_fijos_fk, get_items_energia_fk, get_items_fijos_req, get_items_energia_req, get_tarifas_table
from prepapp.views import SociosList, SociosAlta, SociosModificar, TerrenoList, TerrenoAlta, TerrenoModificar, \
    TarifaList, CespList, CespAlta, CespModificar, sociosSuspender, sociosHabilitar, \
    terrenosSuspender, terrenosHabilitar, ItemsList, ItemsAlta, ItemsModificar, itemsSuspender, itemsHabilitar, \
    sociosSuspender, sociosHabilitar, terrenosSuspender, terrenosHabilitar, tarifaConfiguracion, ImportacionAgua, \
    tarifaEdicion

sociosPatterns = [
    url(r'list/$', SociosList.as_view(), name="SociosList"),
    url(r'new/$', SociosAlta.as_view(), name="SociosAlta"),
    url(r'update/(?P<pk>\d+)$', SociosModificar.as_view(), name="SociosModificar"),
    url(r'suspender/(?P<pk>\d+)$', sociosSuspender, name='SociosSuspender'),
    url(r'habilitar/(?P<pk>\d+)$', sociosHabilitar, name='SociosHabilitar'),
    url(r'get_socios_table/$', get_socios_table, name='get_socios_table'),
    url(r'get_socios_fk/$', get_socios_fk, name='get_socios_fk'),
]

terrenosPatterns = [
    url(r'list/$', TerrenoList.as_view(), name="TerrenosList"),
    url(r'new/$', TerrenoAlta.as_view(), name="TerrenosAlta"),
    url(r'update/(?P<pk>\d+)$', TerrenoModificar.as_view(), name="TerrenosModificar"),
    url(r'suspender/(?P<pk>\d+)$', terrenosSuspender, name='TerrenosSuspender'),
    url(r'habilitar/(?P<pk>\d+)$', terrenosHabilitar, name='TerrenosHabilitar'),
    url(r'get_terrenos_table/$', get_terrenos_table, name='get_terrenos_table'),
]

tarifasPatterns = [
    url(r'list/$', TarifaList.as_view(), name="TarifasList"),
    url(r'new/$', tarifaConfiguracion, name="TarifasAlta"),
    url(r'update/(?P<pk>\d+)$', tarifaEdicion, name="TarifasModificar"),
    url(r'get_tarifas_table/$', get_tarifas_table, name='get_tarifas_table'),
]

cespPatterns = [
    url(r'list/$', CespList.as_view(), name="CespList"),
    url(r'new/$', CespAlta.as_view(), name="CespAlta"),
    url(r'update/(?P<pk>\d+)$', CespModificar.as_view(), name="CespModificar"),
    url(r'get_cesp_table/$', get_cesp_table, name='get_cesp_table'),
]

itemsPatterns = [
    url(r'list/$', ItemsList.as_view(), name="ItemsList"),
    url(r'new/$', ItemsAlta.as_view(), name="ItemsAlta"),
    url(r'update/(?P<pk>\d+)$', ItemsModificar.as_view(), name="ItemsModificar"),
    url(r'get_items_table/$', get_items_table, name='get_items_table'),
    url(r'suspender/(?P<pk>\d+)$', itemsSuspender, name='ItemsSuspender'),
    url(r'habilitar/(?P<pk>\d+)$', itemsHabilitar, name='ItemsHabilitar'),
    url(r'get_items_fijos_fk/$', get_items_fijos_fk, name='get_items_fijos_fk'),
    url(r'get_items_energia_fk/$', get_items_energia_fk, name='get_items_energia_fk'),
    url(r'get_items_fijos_req/$', get_items_fijos_req, name='get_items_fijos_req'),
    url(r'get_items_energia_req/$', get_items_energia_req, name='get_items_energia_req'),
]

cargosFijosPatterns = [
    url(r'importacion/$', ImportacionAgua.as_view(), name="ImportacionAgua"),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^socios/', include(sociosPatterns)),
    url(r'^terrenos/', include(terrenosPatterns)),
    url(r'^tarifas/', include(tarifasPatterns)),
    url(r'^cesp/', include(cespPatterns)),
    url(r'^items/', include(itemsPatterns)),
    url(r'^cargos_fijos/', include(cargosFijosPatterns))
]
