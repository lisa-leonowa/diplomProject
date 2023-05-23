# Подключение модулей для работы с моделями, обработки событий,
# получение измененной информации, проверки номера телефона
import random

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render, redirect
from .models import Clients, ClientsForm
from .forms import SearchClient, NewClient
from .forCyberClass import get_values, client_deals, check_user, form_with_deals, get_user_info, send_message
import re

global cod

def check_fields(value):
    last_name = value[0][0].upper() + value[0][1:].lower()
    first_name = value[1][0].upper() + value[1][1:].lower()
    full_name = value[2][0].upper() + value[2][1:].lower()
    phone = re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', value[4])
    check = bool(phone) and (not any(ch.isdigit() for ch in last_name + first_name + full_name))
    if check:
        return True
    return False


def add_client(valid_form):
    value = get_values(valid_form)
    last_name = value[0][0].upper() + value[0][1:].lower()
    first_name = value[1][0].upper() + value[1][1:].lower()
    full_name = value[2][0].upper() + value[2][1:].lower()
    if check_fields(value):
        return [True, [last_name, first_name, full_name, value[3], value[4], value[5]], value[6]]
    return [False, [last_name, first_name, full_name, value[3], value[4], value[5], value[6]]]


def deleteClient(request, id_user, id_client):
    Clients.objects.filter(id=id_client).delete()  # удаление нужного клиента по id
    return redirect(f'/{id_user}/0')  # переход на основную страницу


# добавление нового клиента
def newClient(request, id_user):
    global cod
    context = {'title': 'Добавление клиента',
               'forms': ClientsForm(),
               'message': 'Добавление клиента',
               'id_user': id_user,
               'user_view': get_user_info(id_user)}  # определение словаря с заголовком страницы
    if request.method == 'POST':
        status = add_client(ClientsForm(request.POST))
        if status[0]:
            status = status[1]
            value = get_values(ClientsForm(request.POST))
            cod = f'Ваш код подтверждения: {random.randint(0, 10)}{random.randint(0, 10)}{random.randint(0, 10)}{random.randint(0, 10)}{random.randint(0, 10)}'
            send_message(value[5], cod)
            form_new_client = NewClient(initial={'last_name': status[0],
                                                 'first_name': status[1],
                                                 'full_name': status[2],
                                                 'gender': value[3],
                                                 'phone': value[4],
                                                 'mail': value[5],
                                                 'remark': value[6]})
            context = {'forms': form_new_client,
                       'id_user': id_user,
                       'title': 'Новый клиент',
                       'message': 'Введите код подтверждения ниже'}
            return render(request, "mail_confirmation.html", context=context)
        else:
            status = status[1]
            context['forms'] = ClientsForm(initial={'last_name': status[0],
                                                    'first_name': status[1],
                                                    'full_name': status[2],
                                                    'gender': status[3],
                                                    'phone': status[4],
                                                    'mail': status[5],
                                                    'remark': status[6], })
            context['message'] = 'Данные были введены неверно!'
    return render(request, "newClient.html", context=context)


# Обновление информации о клиенте
def updateClient(clientform, id_client):
    values = get_values(clientform)  # получение новой информации
    client = Clients.objects.get(id=id_client)  # выбор нужного клиента в базе
    if check_fields(values):
        # изменение информации
        client.last_name = values[0]
        client.first_name = values[1]
        client.full_name = values[2]
        client.gender = values[3]
        client.phone = values[4]
        client.mail = values[5]
        client.remark = values[6]
        client.save()  # сохранение изменения
    return


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
                                                                  'mail': all_clients[i].mail,
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
                                                     'mail': i.mail,
                                                     'remark': i.remark}, )
    return initial_clients


def mail_confirmation(request, id_user):
    global cod
    form = NewClient(request.POST)
    if form.is_valid():
        value = get_values(form)
        if str(value[7]) == str(cod.split()[-1]):
            Clients.objects.create(last_name=value[0],
                                   first_name=value[1],
                                   full_name=value[2],
                                   gender=value[3],
                                   phone=value[4],
                                   mail=value[5],
                                   remark=value[6])
            return redirect(f'/{id_user}/0')
        else:
            context = {'forms': form,
                       'id_user': id_user,
                       'title': 'Новый клиент',
                       'message': 'Код указан неверно!'
                       }
            return render(request, "mail_confirmation.html", context=context)



# работа главной станицы клиентов
def index(request, id_user, id_client):
    context = {'title': 'Система управление клиентами',
               'formSearch': SearchClient(),
               'forms': form_with_deals(get_clients(), client_deals()),
               'id_user': id_user,
               'user_view': get_user_info(id_user)}
    if (request.method == "POST") and (id_client != 0):  # обработка изменения информации
        user_form = ClientsForm(request.POST)  # заполненная форма
        updateClient(user_form, id_client)  # вызов функции обновления информации
        return redirect(f'/{id_user}/0')
    elif (request.method == 'POST') and (id_client == 0):  # обработка поиска и просмотр информации
        search_clients = SearchClient(request.POST)  # заполненная форма поиска
        if search_clients.is_valid():  # если форма отправлена
            context['forms'] = form_with_deals(searchClient(search_clients), client_deals())
            if check_user(id_user) == 'Администратор':
                return render(request, "index.html", context=context)
            else:
                return render(request, "indexDirector.html", context=context)
    if check_user(id_user) == 'Администратор':
        return render(request, "index.html", context=context)
    else:
        return render(request, "indexDirector.html", context=context)
