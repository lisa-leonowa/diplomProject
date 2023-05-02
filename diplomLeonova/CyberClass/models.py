# Подключение модулей для создания моделей
from django.db import models
from django.forms import ModelForm
from django.urls import reverse


# Модель для работы с клиентом
class Clients(models.Model):
    last_name = models.CharField('Фамилия', max_length=100)  # Фамилия
    first_name = models.CharField('Имя', max_length=100)  # Имя
    full_name = models.CharField('Отчество', max_length=100)  # Отчество
    gender = models.CharField('Пол', max_length=1, choices=[('м', 'муж'), ('ж', 'жен')], default='ж')  # Пол
    phone = models.CharField('Номер телефона', max_length=13)  # Номер телефона
    remark = models.CharField('Примечание', max_length=200, null=True, blank=True)  # Примечание


class ClientsForm(ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'


    def form_values(self):
        return ['last_name', 'first_name', 'full_name', 'gender', 'phone', 'remark']



