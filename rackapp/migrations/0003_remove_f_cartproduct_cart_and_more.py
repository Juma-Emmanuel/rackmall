# Generated by Django 4.2.4 on 2023-08-31 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rackapp', '0002_f_cart_pro_duct_f_cartproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='f_cartproduct',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='f_cartproduct',
            name='product',
        ),
        migrations.DeleteModel(
            name='F_Cart',
        ),
        migrations.DeleteModel(
            name='F_CartProduct',
        ),
        migrations.DeleteModel(
            name='Pro_duct',
        ),
    ]
