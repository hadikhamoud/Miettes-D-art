# Generated by Django 4.0.4 on 2022-11-03 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MA', '0056_alter_zone_zone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Country', models.CharField(blank=True, max_length=12, null=True)),
                ('Zone', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MA.zone')),
            ],
        ),
    ]
