# Generated by Django 4.2.7 on 2023-12-12 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0007_imagenes_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenes',
            name='image_url',
            field=models.URLField(),
        ),
    ]
