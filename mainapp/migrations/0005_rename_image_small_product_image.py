# Generated by Django 4.1.7 on 2023-03-25 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_category_image_alter_product_image_large_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image_small',
            new_name='image',
        ),
    ]
