# Generated by Django 4.2 on 2023-05-22 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CyberClass', '0010_clients_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='mail',
            field=models.EmailField(max_length=100, verbose_name='Почта'),
        ),
    ]
