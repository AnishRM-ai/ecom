# Generated by Django 5.0.3 on 2024-05-13 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_remove_order_shipped_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancellationorder',
            name='mark_as_read',
            field=models.BooleanField(default=False),
        ),
    ]