from django import forms


class SearchClient(forms.Form):
    search = forms.CharField(label='', required=False)
    def form_values(self):  # метод возвращающий поля формы
        return ['search']
