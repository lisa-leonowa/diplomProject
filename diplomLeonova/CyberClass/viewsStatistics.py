import os
from .forCyberClass import all_services, get_purchased_services, for_diagram, get_user_info
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect


def index(request, id_user):

    services = all_services()
    purchased_services = get_purchased_services()
    names, values = for_diagram(services, purchased_services)

    plt.figure(figsize=(15, 10), dpi=100)
    plt.grid(which="major", axis='x', color='#000', alpha=0.5, zorder=1)
    plt.grid(which="major", axis='y', color='#000', alpha=0.5, zorder=1)

    plt.subplot()
    plt.bar(names, values, )

    # Plot bars
    bar1 = plt.bar(names, values, color='#1F77B4', width=0.9, zorder=2)

    plt.bar_label(bar1, labels=[f'{e:,.1f}' for e in values], padding=3, color='black', fontsize=8)
    my_path = os.path.dirname(os.path.dirname(__file__))
    plt.savefig(f'{my_path}\\CyberClass\\static\\img\\diagram.png')
    #plt.show()
    context = {'title': 'Статистика продажи курсов',
               'id_user': id_user,
               'user_view': get_user_info(id_user)}
    return render(request, "indexStatistics.html", context=context)
