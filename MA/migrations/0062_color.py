# Generated by Django 4.0.4 on 2022-11-04 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MA', '0061_alter_contactus_options_alter_country_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colorHex', models.CharField(max_length=7, unique=True)),
                ('colorName', models.CharField(max_length=20)),
            ],
        ),
    ]
