# Generated by Django 4.2.7 on 2023-12-09 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operador',
            fields=[
                ('id_operador', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('mail', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Ubicaciones',
            fields=[
                ('id_ubicaciones', models.AutoField(primary_key=True, serialize=False)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('numero_asignacion', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Vuelo',
            fields=[
                ('id_vuelo', models.AutoField(primary_key=True, serialize=False)),
                ('sector_vuelo', models.CharField(max_length=255)),
                ('fecha_vuelo', models.DateField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Imagenes',
            fields=[
                ('id_imagen', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_imagen', models.CharField(max_length=255)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now_add=True)),
                ('vuelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.vuelo')),
            ],
        ),
    ]
