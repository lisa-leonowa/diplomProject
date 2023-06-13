"""
Модуль viewsAuthorization.py
Сторонние библиотеки, используемые в модуле:
shortcuts – библиотека переадресации по маршрутам;
forms - библиотека для работы с формами;
forCyberClass - вспомогательный модуль с набором функций;


Функции, используемые в модуле:
index - обработка страницы авторизации;

Основные переменные:
context - данные передаваемые пользователю;
login - логин пользователя;
password - пароль пользователя;
user_id - идетификатор пользователя в БД;
"""

from django.shortcuts import render, redirect

from .forms import Authorization
from .forCyberClass import get_user, get_values, check_user


def index(request):
    context = {'title': 'Система управление клиентами',
               'form': Authorization(),
               'message': "Добро пожаловать!"}
    if (request.method == 'POST') and (Authorization(request.POST)):
        login, password = get_values(Authorization(request.POST))
        user_id = get_user(login, password)
        if user_id != False:
            context['user_id'] = user_id
            return redirect(f'{user_id}/0')
        else:
            context['message'] = "Логин или пароль были введены неверно!"
    return render(request, "indexAuthorization.html", context=context)
