from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView


class SociosList(TemplateView):
    template_name = "socios/socios_list.html"
