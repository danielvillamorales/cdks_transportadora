from django.db import models
from movimientos.models import Transportadoras, estados_traslados


class Facturas(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateField()
    factura = models.IntegerField(blank=True, null=True)
    nit = models.FloatField(blank=True, null=True)
    tercero = models.CharField(max_length=250, blank=True, null=True)
    direccion = models.CharField(max_length=300, blank=True, null=True)
    ciudad = models.CharField(max_length=30, blank=True, null=True)
    departamento = models.CharField(max_length=30, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    centro_costo = models.CharField(max_length=6, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "facturas"

    def __str__(self) -> str:
        return f"{self.factura} - {self.tercero}"


class EstadoFacturas(models.Model):
    factura = models.OneToOneField(Facturas, models.DO_NOTHING, db_column="factura")
    estado = models.IntegerField(choices=estados_traslados, default=0)
    fecha = models.DateField(null=True, blank=True)
    fecha_generado = models.DateField(null=True, blank=True)
    trasportadora = models.ForeignKey(
        Transportadoras,
        models.DO_NOTHING,
        db_column="trasportadora_id",
        blank=True,
        null=True,
    )
    numero_cajas_1 = models.IntegerField(default=0)
    numero_cajas_2 = models.IntegerField(default=0)
    numero_cajas_3 = models.IntegerField(default=0)

    @property
    def estado_descripcion(self):
        return estados_traslados[self.estado][1]

    class Meta:
        managed = False
        db_table = "estado_facturas"
