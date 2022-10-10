# Generated by Django 3.0.1 on 2021-12-29 14:01

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MA', '0003_auto_20211229_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Color',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10, null=True), blank=True, default=['Gold', 'Silver'], null=True, size=None),
        ),
        migrations.AlterField(
            model_name='product',
            name='Size',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10, null=True), blank=True, default=['XS', 'S', 'M', 'L', 'XL'], null=True, size=None),
        ),
    ]