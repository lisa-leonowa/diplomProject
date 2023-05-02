# Подключение модулей для работы с моделями, обработки событий, получение измененной информации, проверки номера телефона
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render, redirect
from .models import Clients, ClientsForm
from django.http import HttpResponse
import re

from django.contrib.sites.shortcuts import get_current_site
import requests


# получение значений из формы
def get_values(valid_form):
    if valid_form.is_valid():  # если форма была отправлена
        value = []  # массив для хранения значений формы
        for i in valid_form.form_values():  # переборка значений
            value.append(valid_form.cleaned_data[i])  # добавления значения в массив
        return value  # возврат массива с данными
    return "Invalied Data"  # сообщение об ошибке

def add_client(valid_form):
    value = get_values(valid_form)
    last_name = value[0][0].upper() + value[0][1:].lower()
    first_name = value[1][0].upper() + value[1][1:].lower()
    full_name = value[2][0].upper() + value[2][1:].lower()
    phone = re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', value[4])
    check = bool(phone) and (not any(ch.isdigit() for ch in last_name+first_name+full_name))
    if check:
        client = Clients.objects.create(last_name=last_name, first_name=first_name, full_name=full_name, gender=value[3],
                                        phone=value[4], remark=value[5])
        return True
    return [last_name, first_name, full_name, value[3], value[4], value[5]]


# Create your views here.
# добавление нового клиента
def newClient(request):
    context = {'title': 'Добавление клиента'}  # определение словаря с заголовком страницы
    context['forms'] = ClientsForm()  # получение форм всех клиентов
    if (request.method == 'POST'):
        status = add_client(ClientsForm(request.POST))
        if status == True:
            return redirect('/0')
        else:
            context['forms'] = ClientsForm(initial={'last_name': status[0],
                                  'first_name': status[1],
                                  'full_name': status[2],
                                  'gender': status[3],
                                  'phone': status[4],
                                  'remark': status[5],})
            context['message'] = 'Данные были введены неверно!'
    return render(request, "newClient.html", context=context)


# Обновление информации о клиенте
def updateClient(userform, id):
    values = get_values(userform)  # получение новой информации
    client = Clients.objects.get(id=id)  # выбор нужного клиента в базе
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


# работа главной станицы
def index(request, id):
    context = {'title': 'Система управление клиентами'} # определение словаря с заголовком страницы
    if (request.method == "POST") and (id != 0):  # обработка изменения информации
        userform = ClientsForm(request.POST)  # заполненная форма
        updateClient(userform, id)  # вызов функции обновления информации
        return redirect('/0')  # переход на основную страницу

    elif (request.method == 'POST') and (id == 0):  # обработка отображения информации
        pass
    context['forms'] = get_clients()  # получение форм всех клиентов

    return render(request, "index.html", context=context)
