from django.db import models


# Create your models here.
class Traslados(models.Model):
    id = models.IntegerField(primary_key=True)
    numero = models.IntegerField()
    fecha = models.DateField()
    documento_codigo = models.CharField(max_length=6, blank=True, null=True)
    documento_descripcion = models.CharField(max_length=40, blank=True, null=True)
    bodega_origen = models.CharField(max_length=5, blank=True, null=True)
    bodega_destino = models.CharField(max_length=3, blank=True, null=True)
    bodega_destino_desc = models.CharField(max_length=50, blank=True, null=True)
    bodega_destino_direccion = models.CharField(max_length=50, blank=True, null=True)
    telefono_bodega_destino = models.CharField(max_length=12, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    centro_costo = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "traslados"

    def create(self, *args, **kwargs):
        raise NotImplementedError(
            "Este modelo es de solo lectura, no se pueden crear datos."
        )

    def update(self, *args, **kwargs):
        raise NotImplementedError(
            "Este modelo es de solo lectura, no se pueden actualizar datos."
        )

    def delete(self, *args, **kwargs):
        raise NotImplementedError(
            "Este modelo es de solo lectura, no se pueden eliminar datos."
        )

    @property
    def ciudad_destino(self):
        if self.ciudad:
            ciudad = self.ciudad.split("-")
            return ciudad[0].strip() if ciudad else "NN"
        return "NN"

    @property
    def departamento_destino(self):
        if self.ciudad:
            ciudad = self.ciudad.split("-")
            return ciudad[1].strip() if len(ciudad) > 1 else "NN"
        return "NN"

    def __str__(self) -> str:
        return f"{self.bodega_origen} - {self.bodega_destino} - {self.numero}"


estados_traslados = ((0, "trasladado"), (1, "registrado"), (2, "generado"))


class Transportadoras(models.Model):
    descripcion = models.CharField(max_length=50)
    codigo = models.CharField(max_length=5)

    class Meta:
        db_table = "transportadoras"
        unique_together = (("descripcion", "codigo"),)
        permissions = [
            ("generar_guias", "generar_guias"),
            ("ver_traslados", "ver_traslados"),
        ]

    def __str__(self) -> str:
        return f"{self.descripcion} - {self.codigo}"


class EstadosTraslados(models.Model):
    traslado = models.OneToOneField(
        Traslados,
        models.DO_NOTHING,
        db_column="traslado_id",
    )
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
