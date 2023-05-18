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
from CyberClass import viewsClient, viewsService, viewsDeals, viewsStatistics, viewsEmployees, viewsAuthorization

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:id_user>/newClient', viewsClient.newClient),
    path('<int:id_user>/<int:id_client>', viewsClient.index),
    path('<int:id_user>/delete/<int:id_client>', viewsClient.deleteClient),

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
