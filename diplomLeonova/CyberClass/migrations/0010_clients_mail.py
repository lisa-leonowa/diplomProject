# Generated by Django 4.2 on 2023-05-22 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CyberClass', '0009_alter_deals_id_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='mail',
            field=models.CharField(default=123, max_length=100, verbose_name='Почта'),
            preserve_default=False,
        ),
    ]
