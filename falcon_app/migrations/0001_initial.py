# Generated by Django 3.2.9 on 2022-02-09 04:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('password', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('product_title', models.CharField(max_length=50)),
                ('product_size', models.CharField(max_length=10)),
                ('product_price', models.PositiveIntegerField(default=1)),
                ('product_image', models.ImageField(upload_to='images/')),
                ('product_quantity', models.PositiveIntegerField(default=1)),
                ('product_description', models.TextField(default='some_text')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=25)),
                ('company_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.PositiveIntegerField()),
                ('address', models.TextField()),
                ('business_address', models.TextField()),
                ('password', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_created=True, default=django.utils.timezone.now)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='falcon_app.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='falcon_app.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='falcon_app.seller'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_created=True, default=django.utils.timezone.now)),
                ('product_price', models.PositiveIntegerField()),
                ('product_quantity', models.PositiveIntegerField(default=1)),
                ('total_price', models.PositiveIntegerField()),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='falcon_app.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='falcon_app.product')),
            ],
        ),
    ]
