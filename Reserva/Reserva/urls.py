"""Reserva URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
#from Reservar.views import BusListView, BusCreateView, BusUpdateView, BusDeleteView
from Reservar.views import *
app_name = 'Reservar'

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),

    path('buses/', list_bus, name = 'list_bus'),
    path('add_buses/', add_bus, name = 'add_bus'),
    path('edit_buses/<int:pk>/', edit_bus, name = 'edit_bus'),
    path('del_buses/<int:pk>/', del_bus, name = 'del_bus'),

    path('rutas/', list_ruta, name = 'list_ruta'),
    path('add_rutas/', add_ruta, name = 'add_ruta'),
    path('edit_rutas/<int:pk>/', edit_ruta, name = 'edit_ruta'),
    path('del_rutas/<int:pk>/', del_ruta, name = 'del_ruta'),

    path('clientes/', list_cli, name = 'list_cli'),

    path('accounts/', include('django.contrib.auth.urls')),

]
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)