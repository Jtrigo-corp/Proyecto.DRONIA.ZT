# Generated by Django 4.2.7 on 2023-12-19 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0014_remove_imagenes_ubicaciones_remove_vuelo_ubicacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagenes',
            name='ubicacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='map.ubicaciones'),
        ),
    ]
