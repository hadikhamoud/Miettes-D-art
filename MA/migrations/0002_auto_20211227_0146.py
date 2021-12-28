# Generated by Django 3.2.9 on 2021-12-26 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MA', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='Image',
            field=models.ImageField(blank=True, null=True, upload_to='static/images'),
        ),
        migrations.AddField(
            model_name='item',
            name='Optional',
            field=models.CharField(blank=True, choices=[('best seller', 'Best Seller'), ('new arrivals', 'New Arrivals'), ('on sale', 'On Sale')], default='new arrivals', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='Status',
            field=models.CharField(choices=[('active', 'Active'), ('disabled', 'Disabled')], default='Active', max_length=30),
        ),
        migrations.AlterField(
            model_name='item',
            name='Description',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
