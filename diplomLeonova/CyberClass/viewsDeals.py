from django.shortcuts import render, redirect
from .models import Deals, Clients, Services
from .forms import NewDeals
from .forCyberClass import get_values
from datetime import date


def client_deals(request, id_client):
    if NewDeals(request.POST).is_valid():
        value_form_deal = get_values(NewDeals(request.POST))
        add_deals(id_client, int(value_form_deal[0]))
        return redirect('/0')

    client = Clients.objects.get(id=id_client)
    context = {'formDeal': NewDeals(),
               'id_client': id_client,
               'client': f'{client.last_name} {client.first_name} {client.full_name}'}
    return render(request, "add_deal.html", context=context)


def add_deals(id_client, id_service):
    Deals.objects.create(id_client=Clients.objects.get(id=id_client),
                         id_service=Services.objects.get(id=id_service),
                         date_deals=date.today())


def delete_deals(request, id_client):
    deals = Deals.objects.filter(id_client=id_client)
    for i in deals:
        i.delete()
    return redirect('/0')
