# Generated by Django 4.0.4 on 2022-10-11 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MA', '0041_alter_product_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Being_delivered',
            new_name='Shipped',
        ),
    ]
