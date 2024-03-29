# Generated by Django 3.0.1 on 2022-03-14 11:33

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('MA', '0037_auto_20220314_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='City',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='Phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, editable=False, max_length=200, null=True, region=None),
        ),
    ]
