from django.contrib import admin
from .models import Transportadoras, EstadosTraslados


@admin.register(Transportadoras)
class TransportadorasAdmin(admin.ModelAdmin):
    list_display = ["descripcion", "codigo"]


@admin.register(EstadosTraslados)
class EstadosTrasladosAdmin(admin.ModelAdmin):
    list_display = [
        "traslado",
        "estado",
        "fecha",
        "trasportadora",
        "numero_cajas_1",
        "numero_cajas_2",
        "numero_cajas_3",
    ]


# Register your models here.
