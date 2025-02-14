# Generated by Django 5.1.5 on 2025-01-31 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Traslados',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('numero', models.IntegerField()),
                ('fecha', models.DateField()),
                ('documento_codigo', models.CharField(blank=True, max_length=6, null=True)),
                ('documento_descripcion', models.CharField(blank=True, max_length=40, null=True)),
                ('bodega_origen', models.CharField(blank=True, max_length=5, null=True)),
                ('bodega_destino', models.CharField(blank=True, max_length=3, null=True)),
                ('bodega_destino_desc', models.CharField(blank=True, max_length=50, null=True)),
                ('bodega_destino_direccion', models.CharField(blank=True, max_length=50, null=True)),
                ('telefono_bodega_destino', models.CharField(blank=True, max_length=12, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=50, null=True)),
                ('cantidad', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'traslados',
            },
        ),
        migrations.CreateModel(
            name='Transportadoras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=50)),
                ('codigo', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'transportadoras',
                'unique_together': {('descripcion', 'codigo')},
            },
        ),
        migrations.CreateModel(
            name='EstadosTraslados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.IntegerField(choices=[(0, 'trasladado'), (1, 'registrado'), (2, 'generado')], default=0)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('fecha_generado', models.DateField(blank=True, null=True)),
                ('numero_cajas_1', models.IntegerField(default=0)),
                ('numero_cajas_2', models.IntegerField(default=0)),
                ('numero_cajas_3', models.IntegerField(default=0)),
                ('trasportadora', models.ForeignKey(blank=True, db_column='trasportadora_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='movimientos.transportadoras')),
                ('traslado', models.OneToOneField(db_column='traslado_id', on_delete=django.db.models.deletion.DO_NOTHING, to='movimientos.traslados')),
            ],
        ),
    ]
