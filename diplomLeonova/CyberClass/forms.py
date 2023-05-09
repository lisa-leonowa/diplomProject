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
