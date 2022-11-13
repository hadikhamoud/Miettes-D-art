# Generated by Django 4.1.3 on 2022-11-11 08:56

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ("MA", "0078_alter_collection_image_alter_discover_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="Thumbnail",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                force_format="WEBP",
                keep_meta=True,
                null=True,
                quality=40,
                scale=25,
                size=[1920, 1080],
                upload_to="static/images",
            ),
        ),
        migrations.AlterField(
            model_name="collection",
            name="Image",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                force_format="WEBP",
                keep_meta=True,
                null=True,
                quality=75,
                scale=None,
                size=[1920, 1080],
                upload_to="static/images",
            ),
        ),
        migrations.AlterField(
            model_name="discover",
            name="Image",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                force_format="WEBP",
                keep_meta=True,
                null=True,
                quality=75,
                scale=None,
                size=[1920, 1080],
                upload_to="static/images",
            ),
        ),
        migrations.AlterField(
            model_name="picture",
            name="picture",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                force_format="WEBP",
                keep_meta=True,
                null=True,
                quality=75,
                scale=None,
                size=[1920, 1080],
                upload_to="static/images",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="Image",
            field=django_resized.forms.ResizedImageField(
                blank=True,
                crop=None,
                force_format="WEBP",
                keep_meta=True,
                null=True,
                quality=75,
                scale=None,
                size=[1920, 1080],
                upload_to="static/images",
            ),
        ),
    ]