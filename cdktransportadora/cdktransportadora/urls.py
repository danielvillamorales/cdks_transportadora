"""
URL configuration for cdktransportadora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from movimientos.views import (
    actualizar_cajas,
    ver_traslados,
    guardar_cajas,
    ver_traslados_llenados,
    descargar_excel_rango_fechas,
)
from facturacion.views import (
    ver_facturas,
    guardar_cajas_factura,
    actualizar_cajas_facturas,
    descargar_excel_rango_fechas_facturas,
    ver_facturas_llenados,
)

urlpatterns = [
    path(
        "accounts/login/", LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("", LoginView.as_view(template_name="login.html"), name="login"),
    path(
        "accounts/logout/",
        LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
    path("admin/", admin.site.urls),
    path("traslados/", ver_traslados, name="ver_traslados"),
    path("guardar_cajas/", guardar_cajas, name="guardar_cajas"),
    path(
        "ver_traslados_llenados/", ver_traslados_llenados, name="ver_traslados_llenados"
    ),
    path("actualizar_cajas/", actualizar_cajas, name="actualizar_cajas"),
    path(
        "descargar_excel_rango_fechas/",
        descargar_excel_rango_fechas,
        name="descargar_excel_rango_fechas",
    ),
    path("facturas/", ver_facturas, name="ver_facturas"),
    path("guardar_cajas_factura/", guardar_cajas_factura, name="guardar_cajas_factura"),
    path(
        "actualizar_cajas_facturas/",
        actualizar_cajas_facturas,
        name="actualizar_cajas_facturas",
    ),
    path(
        "descargar_excel_rango_fechas_facturas/",
        descargar_excel_rango_fechas_facturas,
        name="descargar_excel_rango_fechas_facturas",
    ),
    path(
        "ver_facturas_llenadas/",
        ver_facturas_llenados,
        name="ver_facturas_llenadas",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
