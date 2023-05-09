from .models import Services, Deals, Clients


def choice_service():
    all_services = Services.objects.all()
    services = ()
    for i in all_services:
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
    all = Services.objects.all()
    for i in all:
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
