# Generated by Django 4.2.2 on 2024-05-30 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_product_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'permissions': [('can_deactivate', 'deactivate product'), ('can_edit_description', 'edit description product'), ('can_edit_category', 'edit category product')], 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]
