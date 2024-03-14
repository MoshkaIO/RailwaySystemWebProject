# Generated by Django 4.2.6 on 2024-01-29 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable', '0022_remove_passanger_doc_info_remove_passanger_doc_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='passanger',
            name='doc_info',
            field=models.CharField(default=8458244, max_length=50, verbose_name='Серия и/или номер документа'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='passanger',
            name='doc_type',
            field=models.CharField(default='Паспорт', max_length=50, verbose_name='Тип документа:'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='passanger',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
