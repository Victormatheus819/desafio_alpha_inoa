# Generated by Django 3.2 on 2022-12-18 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alfaapp', '0007_auto_20221218_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ativos',
            name='email_compra',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='ativos',
            name='email_venda',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
