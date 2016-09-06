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
from django.contrib.auth.decorators import login_required

from prepapp.api import get_socios_fk, get_socios_table, get_terrenos_table, get_items_table, get_cesp_table
from prepapp.views import SociosList, SociosAlta, SociosModificar, TerrenoList, TerrenoAlta, TerrenoModificar, \
    TarifaList, TarifaAlta, TarifaModificar, CespList, CespAlta, CespModificar, EscalonesEnergiaList, \
    EscalonesEnergiaAlta, EscalonesEnergiaModificar, sociosSuspender, sociosHabilitar, terrenosSuspender, \
    terrenosHabilitar, ItemsList, ItemsAlta, ItemsModificar, itemsSuspender, itemsHabilitar

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
    url(r'new/$', TarifaAlta.as_view(), name="TarifasAlta"),
    url(r'update/(?P<pk>\d+)$', TarifaModificar.as_view(), name="TarifasModificar")
]

cespPatterns = [
    url(r'list/$', CespList.as_view(), name="CespList"),
    url(r'new/$', CespAlta.as_view(), name="CespAlta"),
    url(r'update/(?P<pk>\d+)$', CespModificar.as_view(), name="CespModificar"),
    url(r'get_cesp_table/$', get_cesp_table, name='get_cesp_table'),
]

escalonesEnergiaPatterns = [
    url(r'list/$', EscalonesEnergiaList.as_view(), name="EscalonesEnergiaList"),
    url(r'new/$', EscalonesEnergiaAlta.as_view(), name="EscalonesEnergiaAlta"),
    url(r'update/(?P<pk>\d+)$', EscalonesEnergiaModificar.as_view(), name="EscalonesEnergiaModificar")
]

itemsPatterns = [
    url(r'list/$', ItemsList.as_view(), name="ItemsList"),
    url(r'new/$', ItemsAlta.as_view(), name="ItemsAlta"),
    url(r'update/(?P<pk>\d+)$', ItemsModificar.as_view(), name="ItemsModificar"),
    url(r'get_items_table/$', get_items_table, name='get_items_table'),
    url(r'suspender/(?P<pk>\d+)$', itemsSuspender, name='ItemsSuspender'),
    url(r'habilitar/(?P<pk>\d+)$', itemsHabilitar, name='ItemsHabilitar'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^socios/', include(sociosPatterns)),
    url(r'^terrenos/', include(terrenosPatterns)),
    url(r'^tarifas/', include(tarifasPatterns)),
    url(r'^cesp/', include(cespPatterns)),
    url(r'^escalones/', include(escalonesEnergiaPatterns)),
    url(r'^items/', include(itemsPatterns))
]
