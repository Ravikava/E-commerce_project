# Generated by Django 3.2.9 on 2022-02-09 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('falcon_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_price',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
