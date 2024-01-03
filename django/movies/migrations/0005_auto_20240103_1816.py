# Generated by Django 3.2 on 2024-01-03 18:16

import django.core.validators
from django.db import migrations, models
import movies.storage


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_alter_filmwork_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='file_path',
            field=models.FileField(blank=True, null=True, storage=movies.storage.CustomStorage, upload_to='', verbose_name='file_path'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='rating',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0, 'rating не может быть меньше 0'), django.core.validators.MaxValueValidator(100, 'rating  не может быть больше 100')], verbose_name='rating'),
        ),
    ]
