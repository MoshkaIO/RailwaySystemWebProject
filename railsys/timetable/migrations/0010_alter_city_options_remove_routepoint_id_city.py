# Generated by Django 4.2.6 on 2023-11-24 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0009_city_remove_station_id_city_station_city'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Населённый пункт', 'verbose_name_plural': 'Населённые пункты'},
        ),
        migrations.RemoveField(
            model_name='routepoint',
            name='id_city',
        ),
    ]
