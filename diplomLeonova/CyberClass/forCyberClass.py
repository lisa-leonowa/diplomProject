from .models import Services


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
