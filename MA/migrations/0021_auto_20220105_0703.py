# Generated by Django 3.0.1 on 2022-01-05 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MA', '0020_remove_product_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='shop/static/shop/images/')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='Images',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MA.Picture'),
        ),
    ]
