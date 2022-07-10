# Generated by Django 3.0.8 on 2022-07-10 13:42

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20220709_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_detail_img',
            field=models.ImageField(null=True, upload_to=api.models.product_path),
        ),
        migrations.AddField(
            model_name='user',
            name='set_curation',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='brand',
            name='brand_bg_img',
            field=models.ImageField(null=True, upload_to=api.models.brand_path),
        ),
        migrations.AlterField(
            model_name='brand',
            name='brand_logo',
            field=models.ImageField(null=True, upload_to=api.models.brand_path),
        ),
        migrations.AlterField(
            model_name='magazine',
            name='main_img',
            field=models.ImageField(null=True, upload_to=api.models.magazine_path),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_main_img',
            field=models.ImageField(null=True, upload_to=api.models.product_path),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_main_img',
            field=models.ImageField(null=True, upload_to=api.models.review_path),
        ),
        migrations.DeleteModel(
            name='ProductMedia',
        ),
    ]