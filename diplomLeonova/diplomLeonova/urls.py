"""
URL configuration for diplomLeonova project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CyberClass import viewsClient, viewsService, viewsDeals, viewsStatistics, viewsEmployees

urlpatterns = [
    path('admin/', admin.site.urls),
    path('newClient', viewsClient.newClient),
    path('<int:id_client>', viewsClient.index),
    path('delete/<int:id_client>', viewsClient.deleteClient),

    path('services/newService', viewsService.newService),
    path('services/<int:id_service>', viewsService.index),
    path('services/delete/<int:id_service>', viewsService.deleteService),

    path('deals/<int:id_client>', viewsDeals.client_deals),
    path('deals/add/<int:id_client>', viewsDeals.add_deals),
    path('deals/delete/<int:id_client>', viewsDeals.delete_deals),

    path('statistics', viewsStatistics.index),

    path('employees/<int:id_employee>', viewsEmployees.index),
    path('employees/delete/<int:id_employee>', viewsEmployees.deleteEmployees),
    path('employees/newEmployees', viewsEmployees.newEmployees),
    path('employees/new_doc/<int:id_employee>', viewsEmployees.new_doc),

]
