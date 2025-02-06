from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import date, timedelta
from .models import Facturas, EstadoFacturas
from movimientos.models import Transportadoras
from django.contrib import messages
from django.db.models import Q, Sum, F
from django.contrib.auth.models import Group, Permission, User
import openpyxl
from io import BytesIO
from django.contrib.auth.decorators import login_required, permission_required
from movimientos.models import EstadosTraslados
from django.db.models import Value, CharField


@login_required
def ver_facturas(request):
    if request.method == "POST":
        facturas = (
            Facturas.objects.filter(
                factura=request.POST.get("numero_factura"),
            )
            .exclude(id__in=EstadoFacturas.objects.values("factura"))
            .order_by("-fecha")
        )
        if not facturas:
            messages.error(
                request,
                "No se encontraron facturas con los datos ingresados, por favor verifique la información",
            )

    else:
        facturas = (
            Facturas.objects.filter(
                fecha__gte=date.today() - timedelta(days=3),
                fecha__lte=date.today(),
            )
            .exclude(id__in=EstadoFacturas.objects.values("factura"))
            .order_by("fecha", "nit", "ciudad")
        )
    return render(request, "facturas.html", {"facturas": facturas})


@permission_required("movimientos.generar_guias", raise_exception=True)
@login_required
def ver_facturas_llenados(request):
    transportadoras = Transportadoras.objects.all()
    facturas = EstadoFacturas.objects.filter(
        Q(fecha=date.today()) | Q(fecha_generado=date.today()) | Q(estado=1)
    ).order_by("estado", "factura__ciudad", "factura__tercero")
    total_cajas_estado_1 = facturas.filter(estado=1).aggregate(
        total_cajas_1=Sum("numero_cajas_1"),
        total_cajas_2=Sum("numero_cajas_2"),
        total_cajas_3=Sum("numero_cajas_3"),
    )
    total_cajas_estado_2 = facturas.filter(estado=2).aggregate(
        total_cajas_1=Sum("numero_cajas_1"),
        total_cajas_2=Sum("numero_cajas_2"),
        total_cajas_3=Sum("numero_cajas_3"),
    )

    total_cajas_estado_1 = facturas.filter(estado=1).aggregate(
        total_cajas=Sum(F("numero_cajas_1") + F("numero_cajas_2") + F("numero_cajas_3"))
    )
    total_cajas_estado_2 = facturas.filter(estado=2).aggregate(
        total_cajas=Sum(F("numero_cajas_1") + F("numero_cajas_2") + F("numero_cajas_3"))
    )

    total_cajas_estado_1_sum = total_cajas_estado_1["total_cajas"] or 0
    total_cajas_estado_2_sum = total_cajas_estado_2["total_cajas"] or 0
    total_general = total_cajas_estado_1_sum + total_cajas_estado_2_sum

    return render(
        request,
        "factura_llenados.html",
        {
            "facturas": facturas,
            "transportadoras": transportadoras,
            "total_cajas_estado_1_sum": total_cajas_estado_1_sum,
            "total_cajas_estado_2_sum": total_cajas_estado_2_sum,
            "total_general": total_general,
        },
    )


def guardar_cajas_factura(request):
    if request.method == "POST":

        factura_id = request.POST.get("factura_id")
        factura = Facturas.objects.get(id=factura_id)
        caja1 = request.POST.get(f"caja1_{factura_id}")
        caja2 = request.POST.get(f"caja2_{factura_id}")
        caja3 = request.POST.get(f"caja3_{factura_id}")
        estado_traslado = EstadoFacturas.objects.create(
            factura=factura,
            numero_cajas_1=int(caja1),
            numero_cajas_2=int(caja2),
            numero_cajas_3=int(caja3),
            estado=1,
            fecha=date.today(),
        )
        estado_traslado.save()
        messages.success(
            request,
            f"Factura-> {factura.tercero}: {factura.factura}  guardado correctamente",
        )
        return redirect("ver_facturas")


def generar_guia(factura: EstadoFacturas, numero: int):
    lista = []
    cajas = [
        (factura.numero_cajas_1, "CAJA 1", 43, 36, 32, 12),
        (factura.numero_cajas_2, "CAJA 2", 43, 36, 66, 18),
        (factura.numero_cajas_3, "CAJA 3", 74, 36, 66, 25),
        # Agrega más cajas si es necesario
    ]
    for numero_cajas, descripcion_caja, a, b, c, d in cajas:
        if numero_cajas == 0:
            continue
        lista.append(
            [
                "",
                "",
                1,
                0,
                factura.factura.nit,
                factura.factura.tercero,
                factura.factura.direccion,
                factura.factura.ciudad,
                factura.factura.departamento,
                factura.factura.telefono,
                "",
                descripcion_caja,
                "CONFECCIONES",
                "175000",
                numero_cajas,
                1,
                a,
                b,
                c,
                d,
                6,
                2,
                1,
                factura.factura.centro_costo,
                "",
                numero,
                "CM",
                "KG",
                "SER18794",
                factura.factura.factura,
            ]
        )
    return lista


def generar_data_excel(estadosfacturas):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Traslados Actualizados"
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
    numero = 1
    for factura in estadosfacturas:
        guias = generar_guia(factura, numero)
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
    response["Content-Disposition"] = "attachment; filename=facturas_generados.xlsx"
    response.write(excel_file.getvalue())
    return response


def actualizar_cajas_facturas(request):
    if request.method == "POST":
        facturas_ids = request.POST.getlist("factura_id")
        print(facturas_ids)
        facturas = Facturas.objects.filter(id__in=facturas_ids)
        transportadora_id = request.POST.get("transportadora_id")
        print(transportadora_id)
        transportadora = Transportadoras.objects.get(id=transportadora_id)
        estadosfacturas = EstadoFacturas.objects.filter(factura__in=facturas)

        estadosfacturas.update(
            trasportadora=transportadora, estado=2, fecha_generado=date.today()
        )

        # Crear el archivo Excel
        return generar_data_excel(estadosfacturas)

    return redirect("ver_facturas_llenadas")


def descargar_excel_rango_fechas_facturas(request):
    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        estadostraslados = EstadoFacturas.objects.filter(
            fecha_generado__gte=fecha_inicio, fecha_generado__lte=fecha_fin, estado=2
        )
        return generar_data_excel(estadostraslados)

    return redirect("ver_facturas_llenadas")


# Create your views here.


def informes(request):
    if request.method == "POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_final = request.POST.get("fecha_fin")
        facturas = (
            EstadoFacturas.objects.filter(
                fecha_generado__gte=fecha_inicio, fecha_generado__lte=fecha_final
            )
            .annotate(
                tipo=Value("Factura", output_field=CharField()),
                total_cajas=F("numero_cajas_1")
                + F("numero_cajas_2")
                + F("numero_cajas_3"),
            )
            .values(
                "tipo",
                "factura__factura",
                "factura__fecha",
                "factura__nit",
                "factura__tercero",
                "factura__ciudad",
                "factura__direccion",
                "trasportadora__descripcion",
                "fecha_generado",
                "numero_cajas_1",
                "numero_cajas_2",
                "numero_cajas_3",
                "total_cajas",
            )
        )

        traslados = (
            EstadosTraslados.objects.filter(
                fecha_generado__gte=fecha_inicio, fecha_generado__lte=fecha_final
            )
            .annotate(
                tipo=Value("Traslados", output_field=CharField()),
                total_cajas=F("numero_cajas_1")
                + F("numero_cajas_2")
                + F("numero_cajas_3"),
            )
            .values(
                "tipo",
                "traslado__numero",
                "traslado__fecha",
                "traslado__bodega_destino",
                "traslado__bodega_destino_desc",
                "traslado__ciudad",
                "traslado__bodega_destino_direccion",
                "trasportadora__descripcion",
                "fecha_generado",
                "numero_cajas_1",
                "numero_cajas_2",
                "numero_cajas_3",
                "total_cajas",
            )
        )
        # print("facturas")
        # validar_tipos(facturas)
        # print("traslados")
        # validar_tipos(traslados)
        union = unir_data(facturas, traslados)
        return descargar_historico_excel(union)

    return render(request, "informes.html")


def unir_data(facturas, traslados):
    lista = []

    for f in facturas:
        lista.append(
            [
                f.get("tipo"),
                f.get("factura__factura"),
                f.get("factura__fecha"),
                str(f.get("factura__nit")),
                f.get("factura__tercero"),
                f.get("factura__ciudad"),
                f.get("factura__direccion"),
                f.get("trasportadora__descripcion"),
                f.get("fecha_generado"),
                f.get("numero_cajas_1"),
                f.get("numero_cajas_2"),
                f.get("numero_cajas_3"),
                f.get("total_cajas"),
            ]
        )
    for t in traslados:
        lista.append(
            [
                t.get("tipo"),
                t.get("traslado__numero"),
                t.get("traslado__fecha"),
                t.get("traslado__bodega_destino"),
                t.get("traslado__bodega_destino_desc"),
                t.get("traslado__ciudad"),
                t.get("traslado__bodega_destino_direccion"),
                t.get("trasportadora__descripcion"),
                t.get("fecha_generado"),
                t.get("numero_cajas_1"),
                t.get("numero_cajas_2"),
                t.get("numero_cajas_3"),
                t.get("total_cajas"),
            ]
        )
    return lista


def descargar_historico_excel(data):
    wb = openpyxl.Workbook()
    ws = wb.active
    if ws is None:
        return ValueError({"error": "no se pudo generar el excel"})
    ws.title = "Informe De Facturas y Traslados Generados"
    ws.append(
        [
            "tipo",
            "numero",
            "fecha",
            "nit_o_bodega",
            "tercero",
            "ciudad",
            "direccion",
            "transportadora",
            "fecha_generado",
            "cajas_1",
            "cajas_2",
            "cajas_3",
            "total_cajas",
        ]
    )
    for d in data:
        ws.append(d)
    excel = BytesIO()
    wb.save(excel)
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = (
        "attachment; filename=Facturas_Traslados_Generados.xlsx"
    )
    response.write(excel.getvalue())
    return response


def validar_tipos(union):
    for item in union:
        for key, value in item.items():
            print(f"Campo: {key}, Tipo: {type(value)}")
