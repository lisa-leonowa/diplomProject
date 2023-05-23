"""
Дипломный проект по специальности 09.02.07 «Информационные системы и программирование»
по теме «Разработка программной системы управления клиентами предприятия ООО «Кибер класс»».
Название: forCyberClass.py.
Разработал: Леонова Е. А., группа ТИП-81.
Дата и номер версии: 19.05.2023 v3.0.
Язык: Python.
Краткое описание:
Данный модуль отвечает за внутреннюю работу с данными об Услугах, Сделках, Клиентах, Сотрудниками.

Сторонние библиотеки, используемые в программе:
models – модуль, позволяющий работать с объектами базы данных;

Функции, используемые в модуле:
choice_service - функция, преобразовывающая список доступных курсов;
get_values - функция, возвращая данные из формы;
format_date - функция, преобразовывающая дату;
format_deal - функция, преобразовывающая информацию о покупке услуги;
get_id_all_clients - функция, возвращающая информацию о всех клиентах;
client_deals - функция, возвращающая историю покупок всех клиентов;
form_with_deals - функция, преобразовывающая историю покупок клиентов;
all_services - функция, возвращающая информацию о всех услугах;
get_purchased_services - функция, возвращающая данные о сделках всех клиентов;
for_diagram - функция, преобразовывающая данные для составления диаграммы;
check_user - функция, возвращаю роль сотрудника;
get_user - функция, возвращающая идентификатор пользователя из базы данных;

Основные переменные:
all_service - хранит объекты всех услуг;
services - хранить значения объектов услуг;
valid_form - заполненная форма с информацией;
value - массив с данными из формы;
date - дата для преобразования;
day - день для преобразования;
month - месяц для преобразования;
year - год для преобразования;
date_deal - дата покупки услуги;
name_service - наименование купленной услуги;
list_id_clients - массив идентификаторов клиентов;
all_clients - массив всех объектов клиентов;
client_deal - словарь, хранящий информацию о покупках клиентов;
all_deals - массив всех сделок;
client - идентификатор клиента;
answer - словарь, хранящий историю покупок клиентов;
list_id_services - словарь, хранящий информацию о доступных услугах;
purchased_services - словарь услуг, которые приобретались;
list_name - массив заголовков для диаграммы статистики;
list_value - массив значений для диаграммы статистики;
dict_service - словарь всех услуг;
dict_purchased_services - словарь приобретенных услуг;
user - информация о пользователе, который проходит авторизацию;
login - логин, вводимый пользователем в окне авторизации;
password - пароль, вводимый в окне авторизации;
"""

from .models import Services, Deals, Clients, Employees
import smtplib  # Импортируем библиотеку по работе с SMTP

# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML


# генерация меня услуг для покупки
def choice_service():
    all_service = Services.objects.all()
    services = ()
    for i in all_service:
        services += (i.id, i.name_services),
    return services


def get_values(valid_form):
    if valid_form.is_valid():  # если форма была отправлена
        value = []  # массив для хранения значений формы
        for i in valid_form.form_values():  # переборка значений
            value.append(valid_form.cleaned_data[i])  # добавления значения в массив
        return value  # возврат массива с данными
    return "Invalid Data"  # сообщение об ошибке


def format_date(date):  # функция преобразования даты
    day = str(date.day)  # получения дня
    month = str(date.month)  # получение месяца
    year = str(date.year)  # получение года
    if len(day) == 1:  # если в дне 1 цифра, добавляем 0 вначале
        day = '0' + day
    if len(month) == 1:  # если в месяце 1 цифра, добавляет 0 в начале
        month = '0' + month
    return f'{day}.{month}.{year}'  # возврат преобразованной даты


def format_deal(name_service, date_deal):
    date_deal = format_date(date_deal)
    return f'Покупка курса {name_service} была произведена {date_deal}'


def get_id_all_clients():
    list_id_clients = []
    all_clients = Clients.objects.all()
    for i in all_clients:
        list_id_clients.append(i.id)
    return list_id_clients


def client_deals():  # получение информации о сделках всех клиентов
    client_deal = {}
    # получение информации о всех сделках клиентах (отсортированные в обратном порядке)
    all_deals = Deals.objects.order_by('date_deals').reverse()
    for i in all_deals:  # перебор элементов
        if i.id_client.id in client_deal:  # если у клиента уже была хотя бы 1 покупка, добавление последующих
            client = client_deal[i.id_client.id]
            client.append(format_deal(i.id_service.name_services, i.date_deals))
            client_deal[i.id_client.id] = client
        else:  # первая покупка клиента
            client_deal[i.id_client.id] = [format_deal(i.id_service.name_services, i.date_deals)]
    return client_deal  # возврат информации о покупках


def form_with_deals(forms_client, deals, status='all'):
    answer = {}
    for i in forms_client.keys():
        if (i in deals) and (status == 'all'):
            answer[i] = [forms_client[i], deals[i]]
        elif (i not in deals) and (status == 'all'):
            answer[i] = [forms_client[i], ['Курсы пока не приобретались']]
    return answer


def all_services():  # возвращает словарь формата id_курса: наименование курса
    list_id_services = {}
    all_service = Services.objects.all()
    for i in all_service:
        list_id_services[int(i.id)] = i.name_services
    return list_id_services


def get_purchased_services():
    purchased_services = {}
    all_deals = Deals.objects.all()
    for i in all_deals:
        if int(i.id_service.id) in purchased_services:
            purchased_services[int(i.id_service.id)] += 1
        else:
            purchased_services[int(i.id_service.id)] = 1
    return purchased_services


def for_diagram(dict_service, dict_purchased_services):
    list_name = []
    list_value = []
    for i in dict_service.keys():
        list_name.append(dict_service[i])
        if i in dict_purchased_services:
            list_value.append(dict_purchased_services[i])
        else:
            list_value.append(0)
    return [list_name, list_value]


def check_user(id_user):
    user = Employees.objects.get(id=id_user)  # выбор нужного клиента в базе
    return str(user.role)


def get_user(login, password):
    user = Employees.objects.filter(login=login) & Employees.objects.filter(password=password)
    if len(user) != 0:
        return user[0].id
    return False


def get_user_info(id_user):
    try:
        user = Employees.objects.get(id=id_user)
        return f'{user.last_name} {user.first_name}, {user.role}'
    except:
        return 'Пользователь не определен'


def send_message(addr_to, message):
    addr_from = "mailCyberClass@yandex.ru"  # отправитель
    password = "qtujmhsihzfgpqob"  # пароль отправителя

    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # поле отправителя
    msg['To'] = addr_to  # поле получатель
    msg['Subject'] = 'Покупка услуги в «КИБЕР КЛАСС»'  # Тема сообщения
    msg.attach(MIMEText(message, 'plain'))  # Добавляем в сообщение текст

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)  # Создаем объект SMTP
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()  # Выходим
    return
