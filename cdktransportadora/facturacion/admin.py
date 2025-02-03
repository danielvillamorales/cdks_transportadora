from django.contrib import admin
from .models import EstadoFacturas


# Register your models here.
@admin.register(EstadoFacturas)
class EstadoFacturasAdmin(admin.ModelAdmin):
    list_display = (
        "factura",
        "estado",
        "fecha",
        "fecha_generado",
        "trasportadora",
        "numero_cajas_1",
        "numero_cajas_2",
        "numero_cajas_3",
    )
    list_filter = ("estado", "fecha", "fecha_generado", "trasportadora")
    search_fields = ("factura", "trasportadora")
    list_per_page = 10
    list_max_show_all = 100
    list_editable = (
        "estado",
        "fecha",
        "fecha_generado",
        "trasportadora",
        "numero_cajas_1",
        "numero_cajas_2",
        "numero_cajas_3",
    )
    list_display_links = ("factura",)
