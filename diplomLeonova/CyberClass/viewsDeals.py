from django.shortcuts import render, redirect
from .models import Deals, Clients, Services
from .forms import NewDeals
from .forCyberClass import get_values, get_user_info, send_message
from datetime import date


def client_deals(request, id_user, id_client):
    if NewDeals(request.POST).is_valid():
        value_form_deal = get_values(NewDeals(request.POST))
        add_deals(id_client, int(value_form_deal[0]))
        return redirect(f'/{id_user}/0')

    client = Clients.objects.get(id=id_client)
    context = {'formDeal': NewDeals(),
               'id_client': id_client,
               'client': f'{client.last_name} {client.first_name} {client.full_name}',
               'id_user': id_user,
               'user_view': get_user_info(id_user)}
    return render(request, "add_deal.html", context=context)


def add_deals(id_client, id_service):
    client = Clients.objects.get(id=id_client)
    service = Services.objects.get(id=id_service)
    message = f'Здравствуйте! Благодарим Вас, {client.last_name} {client.first_name} {client.full_name}, ' \
              f'за покупку курса: {service.name_services}. Напоминаем о необходимости оплатить услугу в размере {service.price} р., ' \
              f'если вы не оплатили её ранее!' \
              f'\nС уважением, команда «КИБЕР КЛАСС» 😌'
    send_message(client.mail, message)
    Deals.objects.create(id_client=Clients.objects.get(id=id_client),
                         id_service=Services.objects.get(id=id_service),
                         date_deals=date.today())


def delete_deals(request, id_user, id_client):
    deals = Deals.objects.filter(id_client=id_client)
    for i in deals:
        i.delete()
    return redirect(f'/{id_user}/0')
