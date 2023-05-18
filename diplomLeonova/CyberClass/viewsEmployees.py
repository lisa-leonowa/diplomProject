from django.shortcuts import render, redirect
from .models import Employees, EmployeesForm
from .forms import SearchClient
from .forCyberClass import get_values, client_deals, get_id_all_clients, form_with_deals
from docxtpl import DocxTemplate


# получение информации о всех сотрудниках
def get_clients():
    initial_clients = {}  # создание словаря, для хранения значений
    all_clients = Employees.objects.all()  # получение информации о всех сотрудниках
    for i in range(len(all_clients)):  # переборка информации
        # определение полей формы
        initial_clients[all_clients[i].id] = EmployeesForm(initial={'last_name': all_clients[i].last_name,
                                                                    'first_name': all_clients[i].first_name,
                                                                    'login': all_clients[i].login,
                                                                    'password': all_clients[i].password,
                                                                    'role': all_clients[i].role}, )
    return initial_clients  # возврат


def updateEmployee(user_form, id_employee):
    values = get_values(user_form)  # получение новой информации
    employee = Employees.objects.get(id=id_employee)  # выбор нужного клиента в базе
    # изменение информации
    employee.last_name = values[0]
    employee.first_name = values[1]
    employee.login = values[2]
    employee.password = values[3]
    employee.role = values[4]
    employee.save()  # сохранение изменения


def searchEmployee(search):
    initial_employee = {}
    search = get_values(search)[0]  # получение данных из формы поиска
    search_list = Employees.objects.filter(last_name__contains=search)
    for i in search_list:
        initial_employee[i.id] = EmployeesForm(initial={'last_name': i.last_name,
                                                        'first_name': i.first_name,
                                                        'login': i.login,
                                                        'password': i.password,
                                                        'role': i.role, })
    return initial_employee


def index(request, id_employee):
    context = {'title': 'Система управление клиентами',
               'formSearch': SearchClient(),
               'forms': get_clients()}
    if (request.method == "POST") and (id_employee != 0):  # обработка изменения информации
        user_form = EmployeesForm(request.POST)  # заполненная форма
        updateEmployee(user_form, id_employee)  # вызов функции обновления информации
        return redirect('/employees/0')
    elif (request.method == 'POST') and (id_employee == 0):  # обработка поиска и просмотр информации
        search_clients = SearchClient(request.POST)  # заполненная форма поиска
        if search_clients.is_valid():  # если форма отправлена
            context['forms'] = searchEmployee(search_clients)
            return render(request, "indexEmployees.html", context=context)

    return render(request, "indexEmployees.html", context=context)


def add_employee(valid_form):
    value = get_values(valid_form)
    last_name = value[0][0].upper() + value[0][1:].lower()
    first_name = value[1][0].upper() + value[1][1:].lower()
    search_list = Employees.objects.filter(login__contains=value[2])
    if len(search_list) == 0:
        Employees.objects.create(last_name=last_name,
                                 first_name=first_name,
                                 login=value[2],
                                 password=value[3],
                                 role=value[4])
        return [True]
    return [False, [last_name, first_name, value[2], value[3], value[4]]]


def newEmployees(request):
    context = {'title': 'Добавление сотрудника',
               'forms': EmployeesForm(),
               'message': 'Добавление сотрудника'}  # определение словаря с заголовком страницы
    if request.method == 'POST':
        status = add_employee(EmployeesForm(request.POST))
        if status[0]:
            return redirect('/employees/0')
        else:
            status = status[1]
            context['forms'] = EmployeesForm(initial={'last_name': status[0],
                                                      'first_name': status[1],
                                                      'login': status[2],
                                                      'password': status[3],
                                                      'role': status[4], })
            context['message'] = 'Указанный логин уже существует!'
    return render(request, "addEmployees.html", context=context)


def deleteEmployees(request, id_employee):
    Employees.objects.filter(id=id_employee).delete()  # удаление нужного клиента по id
    return redirect('/employees/0')  # переход на основную страницу


def new_doc(request, id_employee):
    employee_db = Employees.objects.get(id=id_employee)  # выбор нужного клиента в базе
    dict_employee = {
        'login': employee_db.login,
        'password': employee_db.password,
        'employee': f'{employee_db.last_name} {employee_db.first_name}'
    }
    doc = DocxTemplate('C:/Users/eliza/PycharmProjects/diplomProject/diplomLeonova/CyberClass.docx')
    doc.render(context=dict_employee)
    doc.save(
        'C:/Users/eliza/Desktop/ЛичныеКабинеты/CyberClass%s.docx' % f'{employee_db.last_name}{employee_db.first_name}')
    return redirect('/employees/0')  # переход на основную страницу
