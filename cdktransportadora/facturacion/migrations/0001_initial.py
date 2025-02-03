# Generated by Django 5.1.5 on 2025-02-03 14:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movimientos', '0002_alter_estadostraslados_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facturas',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('factura', models.IntegerField(blank=True, null=True)),
                ('nit', models.FloatField(blank=True, null=True)),
                ('tercero', models.CharField(blank=True, max_length=250, null=True)),
                ('direccion', models.CharField(blank=True, max_length=300, null=True)),
                ('ciudad', models.CharField(blank=True, max_length=30, null=True)),
                ('departamento', models.CharField(blank=True, max_length=30, null=True)),
                ('cantidad', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'facturas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EstadoFacturas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factura', models.IntegerField(blank=True, null=True)),
                ('estado', models.IntegerField(choices=[(0, 'trasladado'), (1, 'registrado'), (2, 'generado')], default=0)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('fecha_generado', models.DateField(blank=True, null=True)),
                ('numero_cajas_1', models.IntegerField(default=0)),
                ('numero_cajas_2', models.IntegerField(default=0)),
                ('numero_cajas_3', models.IntegerField(default=0)),
                ('trasportadora', models.ForeignKey(blank=True, db_column='trasportadora_id', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='movimientos.transportadoras')),
            ],
            options={
                'db_table': 'estado_facturas',
            },
        ),
    ]
