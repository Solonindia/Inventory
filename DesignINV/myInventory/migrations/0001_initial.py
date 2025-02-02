# Generated by Django 5.0.3 on 2024-11-28 06:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_code', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myInventory.site')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_code', models.CharField(max_length=100)),
                ('material_desc', models.CharField(max_length=255)),
                ('owner', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('opening_stock', models.IntegerField()),
                ('consumption', models.IntegerField(default=0)),
                ('closing_stock', models.IntegerField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myInventory.site')),
            ],
        ),
    ]
