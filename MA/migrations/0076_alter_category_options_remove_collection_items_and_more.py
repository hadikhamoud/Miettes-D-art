# Generated by Django 4.1.3 on 2022-11-10 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MA', '0075_alter_product_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.RemoveField(
            model_name='collection',
            name='Items',
        ),
        migrations.RemoveField(
            model_name='discover',
            name='Items',
        ),
        migrations.AlterField(
            model_name='discover',
            name='Title',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='discover',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
