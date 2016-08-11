from django.contrib import admin

# Register your models here.
from prepapp.models import Socio, Terreno, RecambioMedidor, Tarifa, EscalonesEnergia, Items, Cesp, Factura

admin.site.register(Socio)
admin.site.register(Terreno)
admin.site.register(RecambioMedidor)
admin.site.register(Tarifa)
admin.site.register(EscalonesEnergia)
admin.site.register(Items)
admin.site.register(Cesp)
admin.site.register(Factura)