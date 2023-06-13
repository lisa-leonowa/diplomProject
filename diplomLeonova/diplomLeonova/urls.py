"""
Краткое описание:
Данный модуль отвечает за обработку используемых ссылок в Системе управления клиентами.

Сторонние библиотеки, используемые в программе:
django.contrib – модуль, позволяющий работать в режиме разработчика;
django.urls – модуль, хранящий в себе набор шаблонов, которые обрабатывают полученные ссылки на запрашиваемую страницу,
 позволяют выбрать правильный метод обработки;

Библиотеки, используемые в программе:
CyberClass – самостоятельно написанная библиотека, хранящая в себе набор методов обработки страницы;
"""
from django.contrib import admin
from django.urls import path
from CyberClass import viewsClient, viewsService, viewsDeals, viewsStatistics, viewsEmployees, viewsAuthorization

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:id_user>/newClient', viewsClient.newClient),
    path('<int:id_user>/<int:id_client>', viewsClient.index),
    path('<int:id_user>/delete/<int:id_client>', viewsClient.deleteClient),
    path('<int:id_user>/mail_confirmation', viewsClient.mail_confirmation),

    path('<int:id_user>/services/newService', viewsService.newService),
    path('<int:id_user>/services/<int:id_service>', viewsService.index),
    path('<int:id_user>/services/delete/<int:id_service>', viewsService.deleteService),

    path('<int:id_user>/deals/<int:id_client>', viewsDeals.client_deals),
    path('<int:id_user>/deals/add/<int:id_client>', viewsDeals.add_deals),
    path('<int:id_user>/deals/delete/<int:id_client>', viewsDeals.delete_deals),

    path('<int:id_user>/statistics', viewsStatistics.index),

    path('<int:id_user>/employees/<int:id_employee>', viewsEmployees.index),
    path('<int:id_user>/employees/delete/<int:id_employee>', viewsEmployees.deleteEmployees),
    path('<int:id_user>/employees/newEmployees', viewsEmployees.newEmployees),
    path('<int:id_user>/employees/new_doc/<int:id_employee>', viewsEmployees.new_doc),

    path('', viewsAuthorization.index),
]
