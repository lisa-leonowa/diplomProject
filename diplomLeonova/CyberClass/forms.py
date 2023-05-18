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
    password = forms.CharField(label='Пароль', min_length=8)

    def form_values(self):  # метод возвращающий поля формы
        return ['login', 'password']
