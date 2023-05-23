from django import forms
from .forCyberClass import choice_service


class SearchClient(forms.Form):
    search = forms.CharField(label='', required=False)

    def form_values(self):  # метод возвращающий поля формы
        return ['search']


class NewDeals(forms.Form):
    service = forms.ChoiceField(label='Курс', choices=choice_service)

    def form_values(self):  # метод возвращающий поля формы
        return ['service']


class Authorization(forms.Form):
    login = forms.CharField(label='Логин', min_length=8)
    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput())

    def form_values(self):  # метод возвращающий поля формы
        return ['login', 'password']


class NewClient(forms.Form):
    last_name = forms.CharField(label='Фамилия', max_length=100)  # Фамилия
    first_name = forms.CharField(label='Имя', max_length=100)  # Имя
    full_name = forms.CharField(label='Отчество', max_length=100)  # Отчество
    gender = forms.ChoiceField(label='Пол', choices=(('м', 'муж'), ('ж', 'жен')))  # Пол
    phone = forms.CharField(label='Номер телефона', max_length=13)  # Номер телефона
    mail = forms.EmailField(label='Почта', max_length=100)  # Почта
    remark = forms.CharField(label='Примечание', max_length=200, required=False)  # Примечание
    mail_confirmation = forms.CharField(label='Код подтверждения', max_length=200)  # Код подтверждения

    def form_values(self):
        return ['last_name', 'first_name', 'full_name', 'gender', 'phone', 'mail', 'remark', 'mail_confirmation']
