# Generated by Django 4.2.5 on 2023-09-26 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitacora', '0004_remove_electric_service_code_source_service_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='service_code',
            field=models.IntegerField(),
        ),
    ]
