# Generated by Django 3.0.1 on 2022-03-14 11:33

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('MA', '0038_auto_20220314_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='Phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=200, null=True, region=None),
        ),
    ]
