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

from prepapp.views import SociosList, SociosAlta, SociosModificar, TerrenoList, TerrenoAlta, TerrenoModificar, \
    TarifaList, TarifaAlta, TarifaModificar, CespList, CespAlta, CespModificar, EscalonesEnergiaList, \
    EscalonesEnergiaAlta, EscalonesEnergiaModificar

sociosPatterns = [
    url(r'list/$', SociosList.as_view(), name="SociosList"),
    url(r'new/$', SociosAlta.as_view(), name="SociosAlta"),
    url(r'update/(?P<pk>\d+)$', SociosModificar.as_view(), name="SociosModificar")
]

terrenosPatterns = [
    url(r'list/$', TerrenoList.as_view(), name="TerrenosList"),
    url(r'new/$', TerrenoAlta.as_view(), name="TerrenosAlta"),
    url(r'update/(?P<pk>\d+)$', TerrenoModificar.as_view(), name="TerrenosModificar")
]

tarifasPatterns = [
    url(r'list/$', TarifaList.as_view(), name="TarifasList"),
    url(r'new/$', TarifaAlta.as_view(), name="TarifasAlta"),
    url(r'update/(?P<pk>\d+)$', TarifaModificar.as_view(), name="TarifasModificar")
]

cespPatterns = [
    url(r'list/$', CespList.as_view(), name="CespList"),
    url(r'new/$', CespAlta.as_view(), name="CespAlta"),
    url(r'update/(?P<pk>\d+)$', CespModificar.as_view(), name="CespModificar")
]

escalonesEnergiaPatterns = [
    url(r'list/$', EscalonesEnergiaList.as_view(), name="EscalonesEnergiaList"),
    url(r'new/$', EscalonesEnergiaAlta.as_view(), name="EscalonesEnergiaAlta"),
    url(r'update/(?P<pk>\d+)$', EscalonesEnergiaModificar.as_view(), name="EscalonesEnergiaModificar")
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^socios/', include(sociosPatterns)),
    url(r'^terrenos/', include(terrenosPatterns)),
    url(r'^tarifas/', include(tarifasPatterns)),
    url(r'^cesp/', include(cespPatterns)),
    url(r'^escalones/', include(escalonesEnergiaPatterns))
]
