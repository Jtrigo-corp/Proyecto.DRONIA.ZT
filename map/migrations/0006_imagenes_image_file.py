# Generated by Django 4.2.7 on 2023-12-12 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_vuelo_cantidad_imagenes_vuelo_cantidad_predicciones_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagenes',
            name='image_file',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes/'),
        ),
    ]