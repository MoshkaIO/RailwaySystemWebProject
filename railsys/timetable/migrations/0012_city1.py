# Generated by Django 4.2.6 on 2023-12-06 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0011_seat_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='City1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='НГОРОД ПРОВЕРКА ТАБЛИЦА')),
                ('region', models.CharField(max_length=50, verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'НГОРОД ПРОВЕРКА ТАБЛИЦА',
                'verbose_name_plural': 'НГОРОД ПРОВЕРКА ТАБЛИЦЫ',
            },
        ),
    ]
