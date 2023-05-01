# Подключение модулей для работы с моделями, обработки событий, получение измененной информации
from django.shortcuts import render, redirect
from .models import Clients
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.contrib.sites.shortcuts import get_current_site
import requests


# Create your views here.
# добавление нового клиента
def newClient(request):
    # client = Clients.objects.create(last_name='Халиков', first_name='Раян', full_name='Ренатович', gender='муж', phone='89299861655')
    # print(client.id)
    return HttpResponse('Создал')


def updateClient(request, id):
    response = requests.get(f'http://{get_current_site(request)}/')  # get-запрос
    print('---------------------------------------------------')
    print(response.text)
    print('---------------------------------------------------')
    return HttpResponse('Создал')
    # return redirect('')



# работа главной станицы
def index(request):
    # print(f'Обновление информации {id}')
    # with open(response) as fp:
    #     soup = BeautifulSoup(fp, 'html.parser')  # получаем Html страницу
    # print(soup)
    # find_text = soup.find('div', {'id': f"{id}"})
    # print(find_text)
    # print('---------------')
    # print(find_text.get_text())
    context = {'title': 'Система управление клиентами'}
    context['clients'] = Clients.objects.all()  # получение информации о всех клиентах
    if request.method == "POST":  # обработка загрузки страницы
        pass
    else:  # обработка отправки данных со страницы (клик на кнопку, например)
        pass
    return render(request, "index.html", context=context)
