# Generated by Django 4.2.6 on 2023-11-24 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0004_train'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carriage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carriage_number', models.IntegerField(verbose_name='Номер вагона')),
            ],
        ),
        migrations.CreateModel(
            name='Carriage_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50, verbose_name='Разновидность вагона')),
                ('number_of_Seat', models.IntegerField(verbose_name='Число мест в вагоне')),
            ],
            options={
                'verbose_name': 'Вагон',
                'verbose_name_plural': 'Вагоны',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.train')),
            ],
            options={
                'verbose_name': 'Рейс',
                'verbose_name_plural': 'Рейсы',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(max_length=50, verbose_name='Название станции')),
                ('id_city', models.IntegerField(verbose_name='id населённого пункта')),
            ],
            options={
                'verbose_name': 'Станция',
                'verbose_name_plural': 'Станция',
            },
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_number', models.IntegerField(verbose_name='Номер места')),
                ('place_type', models.CharField(max_length=50, verbose_name='Тип места')),
                ('is_occupied', models.BooleanField(verbose_name='Занято ли место')),
                ('id_carriage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.carriage')),
            ],
        ),
        migrations.CreateModel(
            name='RoutePoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrive_time', models.DateTimeField(verbose_name='Время прибытия')),
                ('departure_time', models.DateTimeField(verbose_name='Время отправления')),
                ('boarding', models.BooleanField(verbose_name='Посадка в поезд')),
                ('id_city', models.IntegerField(verbose_name='ID населённого пункта')),
                ('id_route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.route')),
                ('id_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.station')),
            ],
            options={
                'verbose_name': 'Остановка',
                'verbose_name_plural': 'Остановки',
            },
        ),
        migrations.AddField(
            model_name='carriage',
            name='id_carriage_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.carriage_type'),
        ),
        migrations.AddField(
            model_name='carriage',
            name='id_train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.train'),
        ),
    ]
