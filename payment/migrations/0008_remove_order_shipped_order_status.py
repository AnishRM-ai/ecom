# Generated by Django 5.0.3 on 2024-05-10 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_alter_cancellationorder_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipped',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=25),
        ),
    ]
