# Подключение модулей для создания моделей
from django.db import models


# Модель для работы с клиентом
class Clients(models.Model):
    last_name = models.CharField('last_name', max_length=100)  # Фамилия
    first_name = models.CharField('first_name', max_length=100)  # Имя
    full_name = models.CharField('full_name', max_length=100)  # Отчество
    gender = models.CharField('gender', max_length=1, choices=[('м', 'муж'), ('ж', 'жен')], default='ж')  # Пол
    phone = models.CharField('phone', max_length=13)  # Номер телефона
    remark = models.CharField('remark', max_length=200, null=True)  # Примечание
