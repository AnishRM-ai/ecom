# Generated by Django 5.0.3 on 2024-04-01 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_category_options_category_parent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClothingCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Men'), ('F', 'Female'), ('U', 'Unisex')], max_length=1)),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='clothing_category', to='store.category')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category')),
            ],
        ),
    ]