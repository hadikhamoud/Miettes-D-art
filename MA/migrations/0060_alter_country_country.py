# Generated by Django 4.0.4 on 2022-11-03 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MA', '0059_alter_country_zone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='Country',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
