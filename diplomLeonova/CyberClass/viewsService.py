# Подключение модулей для работы с моделями, обработки событий,
# получение измененной информации
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render, redirect
from .models import Services, ServicesForm
from .forms import SearchClient


# получение значений из формы
def get_values(valid_form):
    if valid_form.is_valid():  # если форма была отправлена
        value = []  # массив для хранения значений формы
        for i in valid_form.form_values():  # переборка значений
            value.append(valid_form.cleaned_data[i])  # добавления значения в массив
        return value  # возврат массива с данными
    return "Invalid Data"  # сообщение об ошибке


# получение информации о всех услугах
def get_services():
    initial_services = {}  # создание словаря, для хранения значений
    all_services = Services.objects.all()  # получение информации о всех услугах
    for i in range(len(all_services)):  # переборка информации
        # определение полей формы
        initial_services[all_services[i].id] = ServicesForm(initial={
            'name_services': all_services[i].name_services,
            'service_duration': all_services[i].service_duration,
            'price': all_services[i].price,
            'description': all_services[i].description, })
    return initial_services  # возврат


# Обновление информации об услуге
def updateService(service_form, id_service):
    values = get_values(service_form)  # получение новой информации
    service = Services.objects.get(id=id_service)  # выбор нужной услуги в базе
    # изменение информации
    service.name_services = values[0]
    service.service_duration = values[1]
    service.price = values[2]
    service.description = values[3]
    service.save()  # сохранение изменения


def add_service(valid_form):
    value = get_values(valid_form)
    Services.objects.create(name_services=value[0],
                            service_duration=value[1],
                            price=value[2],
                            description=value[3])
    return True


# добавление нового курса
def newService(request):
    context = {'title': 'Добавление услуги',
               'forms': ServicesForm()}  # определение словаря с заголовком страницы
    if request.method == 'POST':
        status = add_service(ServicesForm(request.POST))
        if status:
            return redirect('/services/0')
        else:
            context['message'] = 'Данные были введены неверно!'
    return render(request, "newService.html", context=context)


def deleteService(request, id_service):
    Services.objects.filter(id=id_service).delete()  # удаление нужной услуги по id
    return redirect('/services/0')  # переход на основную страницу


def searchService(search):
    initial_clients = {}
    search = get_values(search)[0]  # получение данных из формы поиска
    search_list = Services.objects.filter(name_services__contains=search)

    for i in search_list:
        initial_clients[i.id] = ServicesForm(initial={'name_services': i.name_services,
                                                     'service_duration': i.service_duration,
                                                     'price': i.price,
                                                     'description': i.description}, )
    return initial_clients


# работа главной станицы услуг
def index(request, id_service):
    context = {'title': 'Система управление клиентами',
               'forms': get_services(),
               'formSearch': SearchClient()}  # определение словаря с заголовком страницы
    if (request.method == "POST") and (id_service != 0):  # обработка изменения информации
        user_form = ServicesForm(request.POST)  # заполненная форма
        updateService(user_form, id_service)  # вызов функции обновления информации
        return redirect('/services/0')
    if (request.method == 'POST') and (id_service == 0):  # обработка поиска
        pass
        search_service = SearchClient(request.POST)  # заполненная форма поиска
        if search_service.is_valid():  # если форма отправлена
            context['forms'] = searchService(search_service)  # вызов функции поиска
            return render(request, "indexService.html", context=context)
    return render(request, "indexService.html", context=context)
