from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import date, timedelta
from .models import Traslados, EstadosTraslados, Transportadoras
from django.contrib import messages
from django.db.models import Q, Sum, F
from django.contrib.auth.models import Group, Permission, User
import openpyxl
from io import BytesIO


def ver_traslados(request):
    if request.method == "POST":
        traslados = (
            Traslados.objects.filter(
                bodega_origen=request.POST.get("bodega_origen"),
                numero=request.POST.get("numero_traslado"),
                documento_codigo=request.POST.get("tipo_documento"),
            )
            .exclude(id__in=EstadosTraslados.objects.values("traslado_id"))
            .order_by("fecha")
        )
        if not traslados:
            messages.error(
                request,
                "No se encontraron traslados con los datos ingresados, por favor verifique la información",
            )

    else:
        traslados = (
            Traslados.objects.filter(
                fecha__gte=date.today() - timedelta(days=2),
                fecha__lte=date.today(),
            )
            .exclude(id__in=EstadosTraslados.objects.values("traslado_id"))
            .order_by("fecha")
        )
    return render(request, "movimiento.html", {"traslados": traslados})


def ver_traslados_llenados(request):
    user = get_object_or_404(User, username=request.user)
    if not user.has_perm("transportadoras.generar_guias"):
        messages.error(request, "No tiene permisos para ver esta página")
        redirect("ver_traslados")
    transportadoras = Transportadoras.objects.all()
    traslados = EstadosTraslados.objects.filter(
        Q(fecha=date.today()) | Q(fecha_generado=date.today()) | Q(estado=1)
    ).order_by("estado", "fecha", "traslado__bodega_destino")
    total_cajas_estado_1 = traslados.filter(estado=1).aggregate(
        total_cajas_1=Sum("numero_cajas_1"),
        total_cajas_2=Sum("numero_cajas_2"),
        total_cajas_3=Sum("numero_cajas_3"),
    )
    total_cajas_estado_2 = traslados.filter(estado=2).aggregate(
        total_cajas_1=Sum("numero_cajas_1"),
        total_cajas_2=Sum("numero_cajas_2"),
        total_cajas_3=Sum("numero_cajas_3"),
    )

    total_cajas_estado_1 = traslados.filter(estado=1).aggregate(
        total_cajas=Sum(F("numero_cajas_1") + F("numero_cajas_2") + F("numero_cajas_3"))
    )
    total_cajas_estado_2 = traslados.filter(estado=2).aggregate(
        total_cajas=Sum(F("numero_cajas_1") + F("numero_cajas_2") + F("numero_cajas_3"))
    )

    total_cajas_estado_1_sum = total_cajas_estado_1["total_cajas"] or 0
    total_cajas_estado_2_sum = total_cajas_estado_2["total_cajas"] or 0
    total_general = total_cajas_estado_1_sum + total_cajas_estado_2_sum

    return render(
        request,
        "traslados_llenados.html",
        {
            "traslados": traslados,
            "transportadoras": transportadoras,
            "total_cajas_estado_1_sum": total_cajas_estado_1_sum,
            "total_cajas_estado_2_sum": total_cajas_estado_2_sum,
            "total_general": total_general,
        },
    )


def guardar_cajas(request):
    if request.method == "POST":

        traslado_id = request.POST.get("traslado_id")
        traslado = Traslados.objects.get(id=traslado_id)
        caja1 = request.POST.get(f"caja1_{traslado_id}")
        caja2 = request.POST.get(f"caja2_{traslado_id}")
        caja3 = request.POST.get(f"caja3_{traslado_id}")
        estado_traslado = EstadosTraslados.objects.create(
            traslado=traslado,
            numero_cajas_1=int(caja1),
            numero_cajas_2=int(caja2),
            numero_cajas_3=int(caja3),
            estado=1,
            fecha=date.today(),
        )
        estado_traslado.save()
        messages.success(
            request,
            f"Traslado {traslado.bodega_origen}: {traslado.numero}  guardado correctamente",
        )
        return redirect("ver_traslados")


def generar_guia(traslado: EstadosTraslados, numero: int):
    lista = []
    if traslado.numero_cajas_1 > 0:
        lista.append(
            [
                "",
                "",
                1,
                0,
                traslado.traslado.bodega_destino,
                traslado.traslado.bodega_destino_desc,
                traslado.traslado.bodega_destino_direccion,
                traslado.traslado.ciudad_destino,
                traslado.traslado.departamento_destino,
                traslado.traslado.telefono_bodega_destino,
                "",
                "CAJA 1",
                "CONFECCIONES",
                "175000",
                traslado.numero_cajas_1,
                1,
                43,
                36,
                32,
                12,
                6,
                2,
                1,
                33307,
                "",
                numero,
                "CM",
                "KG",
                "SER18794",
                traslado.traslado.numero,
            ]
        )
    if traslado.numero_cajas_2 > 0:
        lista.append(
            [
                "",
                "",
                1,
                0,
                traslado.traslado.bodega_destino,
                traslado.traslado.bodega_destino_desc,
                traslado.traslado.bodega_destino_direccion,
                traslado.traslado.ciudad_destino,
                traslado.traslado.departamento_destino,
                traslado.traslado.telefono_bodega_destino,
                "",
                "CAJA 2",
                "CONFECCIONES",
                "175000",
                traslado.numero_cajas_2,
                1,
                43,
                36,
                66,
                18,
                6,
                2,
                1,
                33307,
                "",
                numero,
                "CM",
                "KG",
                "SER18794",
                traslado.traslado.numero,
            ]
        )
    if traslado.numero_cajas_3 > 0:
        lista.append(
            [
                "",
                "",
                1,
                0,
                traslado.traslado.bodega_destino,
                traslado.traslado.bodega_destino_desc,
                traslado.traslado.bodega_destino_direccion,
                traslado.traslado.ciudad_destino,
                traslado.traslado.departamento_destino,
                traslado.traslado.telefono_bodega_destino,
                "",
                "CAJA 3",
                "CONFECCIONES",
                "175000",
                traslado.numero_cajas_3,
                1,
                74,
                36,
                66,
                25,
                6,
                2,
                1,
                33307,
                "",
                numero,
                "CM",
                "KG",
                "SER18794",
                traslado.traslado.numero,
            ]
        )
    return lista


def actualizar_cajas(request):
    if request.method == "POST":
        traslado_ids = request.POST.getlist("traslado_ids")
        print(traslado_ids)
        traslados = Traslados.objects.filter(id__in=traslado_ids)
        transportadora_id = request.POST.get("transportadora_id")
        print(transportadora_id)
        transportadora = Transportadoras.objects.get(id=transportadora_id)
        estadostraslados = EstadosTraslados.objects.filter(traslado__in=traslados)

        estadostraslados.update(
            trasportadora=transportadora, estado=2, fecha_generado=date.today()
        )

        # Crear el archivo Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Traslados Actualizados"

        # Agregar encabezados
        ws.append(
            [
                "# referencia",
                "# guia",
                "tiempo",
                "generar sobreporte",
                "doc identificacion",
                "Nombre del Destinatario",
                "Dirección",
                "Ciudad/Cód DANE de destino",
                "departamente",
                "teléfono",
                "celular",
                "tipo caja",
                "Dice Contener",
                "Valor declarado",
                "Número de Piezas",
                "Cantidad",
                "Alto",
                "Ancho",
                "Largo",
                "Peso",
                "Producto",
                "Forma de Pago",
                "Medio de Transporte",
                "Campo personalizado 1",
                "Generar Cajaporte",
                "Identificador de Archivo Origen",
                "Unidad de longitud",
                "Unidad de peso",
                "Codigo de Facturación",
                "factura",
            ]
        )

        # Agregar datos de los traslados actualizados
        for traslado in estadostraslados:
            numero = 0
            guias = generar_guia(traslado, numero)
            if len(guias) > 0:
                numero += 1
            for guia in guias:
                ws.append(guia)

        # Guardar el archivo en memoria
        excel_file = BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)

        # Enviar el archivo como respuesta
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = (
            "attachment; filename=traslados_generados.xlsx"
        )
        response.write(excel_file.getvalue())
        return response

    return redirect("ver_traslados_llenados")


# Create your views here.
