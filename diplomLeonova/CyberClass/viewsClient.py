# Подключение модулей для работы с моделями, обработки событий,
# получение измененной информации, проверки номера телефона
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render, redirect
from .models import Clients, ClientsForm
from .forms import SearchClient
from .forCyberClass import get_values, client_deals, get_id_all_clients, form_with_deals
import re


def add_client(valid_form):
    value = get_values(valid_form)
    last_name = value[0][0].upper() + value[0][1:].lower()
    first_name = value[1][0].upper() + value[1][1:].lower()
    full_name = value[2][0].upper() + value[2][1:].lower()
    phone = re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', value[4])
    check = bool(phone) and (not any(ch.isdigit() for ch in last_name + first_name + full_name))
    if check:
        Clients.objects.create(last_name=last_name,
                               first_name=first_name,
                               full_name=full_name,
                               gender=value[3],
                               phone=value[4],
                               remark=value[5])
        return [True]
    return [False, [last_name, first_name, full_name, value[3], value[4], value[5]]]


def deleteClient(request, id_client):
    Clients.objects.filter(id=id_client).delete()  # удаление нужного клиента по id
    return redirect('/0')  # переход на основную страницу


# добавление нового клиента
def newClient(request):
    context = {'title': 'Добавление клиента',
               'forms': ClientsForm(),
               'message': 'Добавление клиента'}  # определение словаря с заголовком страницы
    if request.method == 'POST':
        status = add_client(ClientsForm(request.POST))
        if status[0]:
            return redirect('/0')
        else:
            status = status[1]
            context['forms'] = ClientsForm(initial={'last_name': status[0],
                                                    'first_name': status[1],
                                                    'full_name': status[2],
                                                    'gender': status[3],
                                                    'phone': status[4],
                                                    'remark': status[5], })
            context['message'] = 'Данные были введены неверно!'
    return render(request, "newClient.html", context=context)


# Обновление информации о клиенте
def updateClient(clientform, id_client):
    values = get_values(clientform)  # получение новой информации
    client = Clients.objects.get(id=id_client)  # выбор нужного клиента в базе
    # изменение информации
    client.last_name = values[0]
    client.first_name = values[1]
    client.full_name = values[2]
    client.gender = values[3]
    client.phone = values[4]
    client.remark = values[5]
    client.save()  # сохранение изменения


# получение информации о всех клиентах
def get_clients():
    initial_clients = {}  # создание словаря, для хранения значений
    all_clients = Clients.objects.all()  # получение информации о всех клиентах
    for i in range(len(all_clients)):  # переборка информации
        # определение полей формы
        initial_clients[all_clients[i].id] = ClientsForm(initial={'last_name': all_clients[i].last_name,
                                                                  'first_name': all_clients[i].first_name,
                                                                  'full_name': all_clients[i].full_name,
                                                                  'gender': all_clients[i].gender,
                                                                  'phone': all_clients[i].phone,
                                                                  'remark': all_clients[i].remark}, )
    return initial_clients  # возврат


def searchClient(search):
    initial_clients = {}
    search = get_values(search)[0]  # получение данных из формы поиска
    search_list_last_name = Clients.objects.filter(last_name__contains=search)
    search_list_phone = Clients.objects.filter(phone__contains=search)
    if len(search_list_last_name) != 0:
        search_list = search_list_last_name
    else:
        search_list = search_list_phone
    for i in search_list:
        initial_clients[i.id] = ClientsForm(initial={'last_name': i.last_name,
                                                     'first_name': i.first_name,
                                                     'full_name': i.full_name,
                                                     'gender': i.gender,
                                                     'phone': i.phone,
                                                     'remark': i.remark}, )
    return initial_clients


# работа главной станицы клиентов
def index(request, id_client):
    context = {'title': 'Система управление клиентами',
               'formSearch': SearchClient(),
               'forms': form_with_deals(get_clients(), client_deals())}
    if (request.method == "POST") and (id_client != 0):  # обработка изменения информации
        user_form = ClientsForm(request.POST)  # заполненная форма
        updateClient(user_form, id_client)  # вызов функции обновления информации
        return redirect('/0')
    elif (request.method == 'POST') and (id_client == 0):  # обработка поиска и просмотр информации
        search_clients = SearchClient(request.POST)  # заполненная форма поиска
        if search_clients.is_valid():  # если форма отправлена
            context['forms'] = form_with_deals(searchClient(search_clients), client_deals())
            return render(request, "index.html", context=context)

    return render(request, "index.html", context=context)
