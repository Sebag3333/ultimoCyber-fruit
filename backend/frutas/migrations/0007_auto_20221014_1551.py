# Generated by Django 3.2.15 on 2022-10-14 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frutas', '0006_stocktienda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='pedido_direccion',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='pedido_fecha',
            field=models.DateField(null=True),
        ),
    ]
