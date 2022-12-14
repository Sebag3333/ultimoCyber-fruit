# Generated by Django 3.2.15 on 2022-10-25 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frutas', '0008_auto_20221014_1737'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contrato',
            old_name='apellido_m',
            new_name='contrato_ape_m',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='apellido_p',
            new_name='contrato_ape_p',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='cargo',
            new_name='contrato_cargo',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='nombres',
            new_name='contrato_estado',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='fecha_i',
            new_name='contrato_fecha_i',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='fecha_t',
            new_name='contrato_fecha_t',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='id',
            new_name='contrato_id',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='rut',
            new_name='contrato_rut',
        ),
        migrations.RenameField(
            model_name='contrato',
            old_name='sueldo',
            new_name='contrato_sueldo',
        ),
        migrations.AddField(
            model_name='contrato',
            name='contrato_nombres',
            field=models.CharField(default=False, max_length=100),
        ),
    ]
