# Generated by Django 3.2 on 2022-12-14 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alfaapp', '0002_ativos_cotacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ativos',
            name='cotacao',
            field=models.FloatField(null=True),
        ),
    ]