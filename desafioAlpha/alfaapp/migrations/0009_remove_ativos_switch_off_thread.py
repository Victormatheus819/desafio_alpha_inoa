# Generated by Django 3.2 on 2022-12-20 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alfaapp', '0008_auto_20221218_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ativos',
            name='switch_off_thread',
        ),
    ]
