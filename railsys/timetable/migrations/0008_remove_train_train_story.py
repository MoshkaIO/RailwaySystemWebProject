# Generated by Django 4.2.6 on 2023-11-24 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0007_train_train_story'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='train',
            name='train_story',
        ),
    ]
