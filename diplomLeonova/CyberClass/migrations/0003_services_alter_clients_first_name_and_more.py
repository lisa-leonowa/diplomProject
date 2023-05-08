# Generated by Django 4.2 on 2023-05-07 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CyberClass', '0002_remove_clients_clientid_clients_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_services', models.CharField(max_length=100, verbose_name='Название курса')),
                ('service_duration', models.CharField(max_length=100, verbose_name='Длительность')),
                ('price', models.IntegerField(verbose_name='Стоимость')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Описание курса')),
            ],
        ),
        migrations.AlterField(
            model_name='clients',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='full_name',
            field=models.CharField(max_length=100, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='gender',
            field=models.CharField(choices=[('м', 'муж'), ('ж', 'жен')], default='ж', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='phone',
            field=models.CharField(max_length=13, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='remark',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Примечание'),
        ),
    ]
