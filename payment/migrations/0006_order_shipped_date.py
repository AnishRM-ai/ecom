# Generated by Django 5.0.3 on 2024-05-08 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_cancellationorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
