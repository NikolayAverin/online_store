# Generated by Django 5.0.4 on 2024-05-14 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_product_photo_version'),
    ]

    operations = [
        migrations.RenameField(
            model_name='version',
            old_name='is_active',
            new_name='activity',
        ),
    ]
