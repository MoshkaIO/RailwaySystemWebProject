# Generated by Django 4.2.6 on 2023-12-15 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0014_route_id_train_alter_routepoint_arrive_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dep_st_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Название станции отправления')),
                ('arr_st_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Название станции')),
                ('dep_time', models.DateTimeField(blank=True, null=True, verbose_name='Время отправления')),
                ('arr_time', models.DateTimeField(blank=True, null=True, verbose_name='Время прибытия')),
            ],
        ),
        migrations.DeleteModel(
            name='City1',
        ),
        migrations.AlterField(
            model_name='routepoint',
            name='arrive_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время прибытия'),
        ),
        migrations.AlterField(
            model_name='routepoint',
            name='departure_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время отправления'),
        ),
    ]
