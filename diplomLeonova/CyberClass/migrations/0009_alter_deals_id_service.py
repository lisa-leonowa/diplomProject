# Generated by Django 4.2 on 2023-05-18 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CyberClass', '0008_employees_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deals',
            name='id_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CyberClass.services'),
        ),
    ]
