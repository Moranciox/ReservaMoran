from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Reservar.views import *

app_name = 'Reservar'

urlpatterns = [
    path('', home, name='home'),  # Redirige a la página de inicio
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),

    path('list_buses/', list_bus, name='list_buses'),
    path('add_buses/', add_bus, name='add_bus'),
    path('edit_buses/<int:pk>/', edit_bus, name='edit_bus'),
    path('del_buses/<int:pk>/', del_bus, name='del_bus'),

    path('rutas/', list_ruta, name='list_ruta'),
    path('add_rutas/', add_ruta, name='add_ruta'),
    path('edit_rutas/<int:pk>/', edit_ruta, name='edit_ruta'),
    path('del_rutas/<int:pk>/', del_ruta, name='del_ruta'),

    path('clientes/', list_cli, name='list_cli'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('disponibilidades/', list_disponibilidad, name='list_disponibilidad'),
    path('disponibilidades/add/', add_disponibilidad, name='add_disponibilidad'),
    path('disponibilidades/edit/<int:pk>/', edit_disponibilidad, name='edit_disponibilidad'),
    path('disponibilidades/del/<int:pk>/', del_disponibilidad, name='del_disponibilidad'),

    path('reserva/', buscar_rutas, name='buscar_rutas'),
    path('reserva/<int:disponibilidad_id>/', reserva_pasaje, name='reserva_pasaje'),
    path('cliente/<int:cliente_id>/reservas/', lista_reservas_cliente, name='lista_reservas_cliente'),
    path('viajes-disponibles/', viajes_disponibles, name='viajes_disponibles'),
    path('about_us/', about_us, name='about_us'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
