# Generated by Django 3.2.22 on 2023-12-10 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobertura', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='node',
            old_name='suscriber',
            new_name='subscriber',
        ),
    ]
