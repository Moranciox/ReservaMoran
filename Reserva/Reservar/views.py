from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Bus, Ruta, Cliente, Disponibilidad, Asientos, Reserva
##from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import BusForm, RutaForm, CliForm, DisponibilidadForm, BusquedaRutasForm, ClienteForm
def reserva_pasaje(request, disponibilidad_id):
    disponibilidad = get_object_or_404(Disponibilidad, id=disponibilidad_id)

    # Obtener los asientos disponibles para esta disponibilidad
    asientos_disponibles = Asientos.objects.filter(
        bus=disponibilidad.bus,
        estado=True,  # Marcamos el estado como disponible
        disponibilidad__fecha=disponibilidad.fecha,
        disponibilidad__horario=disponibilidad.horario
    )

    if request.method == 'POST':
        # Obtener los asientos seleccionados y la información del cliente del formulario
        asientos_seleccionados = request.POST.getlist('asientos')
        cliente_form = ClienteForm(request.POST)

        if cliente_form.is_valid():
            cliente = cliente_form.save()  # Guardar los datos del cliente en la base de datos

            for asiento_numero in asientos_seleccionados:
                # Buscar el asiento seleccionado
                asiento = Asientos.objects.get(bus=disponibilidad.bus, numero=asiento_numero)

                # Asignar el cliente y el asiento seleccionado a la disponibilidad
                disponibilidad.cliente = cliente
                disponibilidad.asiento = asiento

                # Cambiar el estado del asiento a no disponible
                asiento.estado = False
                asiento.save()

                # Marcar la disponibilidad como no disponible
                disponibilidad.disponible = False
                disponibilidad.save()

                # Crear y guardar la reserva con las fechas correctas
                reserva = Reserva(
                    fechaReserva=timezone.now(),  # Fecha y hora actual de la reserva
                    fechaCreacion=timezone.now(),  # Fecha de creación de la reserva (fecha actual)
                    cantidadPasajes=1,  # Puedes ajustar esto según tus necesidades
                    cliente=cliente,
                    ruta=disponibilidad.ruta,
                    bus=disponibilidad.bus,
                    asiento=asiento,
                )
                reserva.save()

            # Redirigir a una página de confirmación o a donde desees
            return render(request, 'cliente/confirmacion_reserva.html', {'disponibilidad': disponibilidad, 'cliente': cliente})

    else:
        cliente_form = ClienteForm()

    contexto = {
        'disponibilidad': disponibilidad,
        'asientos_disponibles': asientos_disponibles,
        'cliente_form': cliente_form,
    }
    return render(request, 'cliente/reserva_pasaje.html', contexto)

def buscar_rutas(request):
    if request.method == 'GET':
        # Obtener los parámetros del formulario de búsqueda
        origen = request.GET.get('origen')
        fecha = request.GET.get('fecha')
        hora = request.GET.get('hora')

        # Realizar el filtrado de disponibilidades basado en los parámetros de búsqueda
        disponibilidades = Disponibilidad.objects.all()
        if origen:
            disponibilidades = disponibilidades.filter(ruta__origen__icontains=origen)
        if fecha:
            disponibilidades = disponibilidades.filter(fecha=fecha)
        if hora:
            disponibilidades = disponibilidades.filter(horario__contains=hora)

        # Pasar los resultados al template
        context = {
            'disponibilidades': disponibilidades,
        }
        return render(request, 'cliente/reserva.html', context)

    return render(request, 'cliente/reserva.html')
@login_required
def index(request):
    return render(request, 'index.html')
    
def home(request):
    return render(request, 'home.html')

@login_required
def list_cli(request):
    clientes = Cliente.objects.all()
    contexto = {
        'clientes':clientes
    }   
    return render(request, 'Clientes/list_clientes.html', contexto)


@login_required
def list_bus(request):
    buses = Bus.objects.all()
    contexto = {
        'buses':buses
    }   
    return render(request, 'buses/list_buses.html', contexto)

@login_required
def add_bus(request):
    if request.method == 'POST':
        bus_form = BusForm(request.POST)
        if bus_form.is_valid():
            temp = bus_form.save(commit=False)
            temp.author = request.user
            temp.save()
            messages.success(request, 'Bus ingresado.')
        else:
            messages.error('Error')

    bus_form = BusForm()
    contexto = {
        'form':bus_form,
    }   
    return render(request, 'buses/add_buses.html', contexto)

@login_required
def edit_bus(request, pk):
    bus = Bus.objects.get(id=pk)
    if request.method == 'POST':
        bus_form = BusForm(request.POST, instance=bus)
        if bus_form.is_valid():
            temp = bus_form.save(commit=False)
            temp.save()
            messages.success(request, 'Bus Actualizado')
        else:
            messages.error('No se pudo actualizar.')
    else:
        bus_form = BusForm(instance=bus)

    contexto = {
        'form':bus_form,
        'bus': bus,
    }
    return render(request, 'buses/edit_buses.html', contexto)

@login_required
def del_bus(request, pk):
    bus = Bus.objects.get(id=pk)
    if request.method == 'POST':
        bus.delete()
        return redirect('list_buses')

    contexto = {
        'bus': bus,
    }
    return render(request, 'buses/del_buses.html', contexto)


@login_required
def list_ruta(request):
    rutas = Ruta.objects.all()
    contexto = {
        'rutas':rutas
    }   
    return render(request, 'rutas/list_rutas.html', contexto)

@login_required
def add_ruta(request):
    if request.method == 'POST':
        ruta_form = RutaForm(request.POST)
        if ruta_form.is_valid():
            temp = ruta_form.save(commit=False)
            temp.author = request.user
            temp.save()
            messages.success(request, 'Ruta ingresada.')
        else:
            messages.error('Error')

    ruta_form = RutaForm()
    contexto = {
        'form':ruta_form,
    }   
    return render(request, 'rutas/add_rutas.html', contexto)

@login_required
def edit_ruta(request, pk):
    ruta = Ruta.objects.get(id=pk)
    if request.method == 'POST':
        ruta_form = RutaForm(request.POST, instance=ruta)
        if ruta_form.is_valid():
            temp = ruta_form.save(commit=False)
            temp.save()
            messages.success(request, 'Ruta Actualizada')
        else:
            messages.error('Ruta no actualizada.')
    else:
        ruta_form = RutaForm(instance=ruta)

    contexto = {
        'form':ruta_form,
        'ruta': ruta,
    }
    return render(request, 'rutas/edit_rutas.html', contexto)

@login_required
def del_ruta(request, pk):
    ruta = Ruta.objects.get(id=pk)
    if request.method == 'POST':
        ruta.delete()
        return redirect('list_ruta')
    contexto = {
        'ruta': ruta,
    }
    return render(request, 'rutas/del_rutas.html', contexto)

def list_disponibilidad(request):
    disponibilidades = Disponibilidad.objects.all()
    buses = Bus.objects.all()
    
    
    context = {
        'disponibilidades': disponibilidades,
    
    }
    
    return render(request, 'disponibilidad/list_disponibilidad.html', context)

@login_required
def add_disponibilidad(request):
    if request.method == 'POST':
        disponibilidad_form = DisponibilidadForm(request.POST)
        if disponibilidad_form.is_valid():
            disponibilidad_form.save()
            return redirect('list_disponibilidad')
    else:
        disponibilidad_form = DisponibilidadForm()

    # Generar lista de horas desde las 6 AM hasta las 11 PM
    hours = []
    current_hour = datetime(2023, 1, 1, 6, 0)  # 6:00 AM
    while current_hour <= datetime(2023, 1, 1, 23, 0):  # 11:00 PM
        hours.append(current_hour.strftime('%H:%M'))
        current_hour += timedelta(hours=1)

    contexto = {
        'form': disponibilidad_form,
        'hours': hours
    }
    return render(request, 'disponibilidad/add_disponibilidad.html', contexto)

@login_required
def edit_disponibilidad(request, pk):
    disponibilidad = get_object_or_404(Disponibilidad, pk=pk)

    if request.method == 'POST':
        form = DisponibilidadForm(request.POST, instance=disponibilidad)
        if form.is_valid():
            form.save()
            return redirect('list_disponibilidad')
    else:
        form = DisponibilidadForm(instance=disponibilidad)

    context = {
        'form': form,
    }
    return render(request, 'disponibilidad/edit_disponibilidad.html', context)

def del_disponibilidad(request, pk):
    disponibilidad = get_object_or_404(Disponibilidad, pk=pk)

    if request.method == 'POST':
        disponibilidad.delete()
        return redirect('list_disponibilidad')

    context = {
        'disponibilidad': disponibilidad,
    }
    return render(request, 'disponibilidad/del_disponibilidad.html', context)

def list_asientos(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    asientos = bus.asientos.all()
    return render(request, 'asiento/list_asientos.html', {'bus': bus, 'asientos': asientos})

def add_asiento(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)

    if request.method == 'POST':
        asiento_form = AsientoForm(request.POST)
        if asiento_form.is_valid():
            asiento = asiento_form.save(commit=False)
            asiento.bus = bus
            asiento.save()
            return redirect('list_asientos', bus_id=bus_id)

    asiento_form = AsientoForm()
    return render(request, 'asiento/add_asiento.html', {'bus': bus, 'form': asiento_form})

def edit_asiento(request, bus_id, asiento_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    asiento = get_object_or_404(Asiento, pk=asiento_id)

    if request.method == 'POST':
        asiento_form = AsientoForm(request.POST, instance=asiento)
        if asiento_form.is_valid():
            asiento_form.save()
            return redirect('list_asientos', bus_id=bus_id)

    asiento_form = AsientoForm(instance=asiento)
    return render(request, 'asiento/edit_asiento.html', {'bus': bus, 'form': asiento_form})

def del_asiento(request, bus_id, asiento_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    asiento = get_object_or_404(Asiento, pk=asiento_id)

    if request.method == 'POST':
        asiento.delete()
        return redirect('list_asientos', bus_id=bus_id)

    return render(request, 'asiento/del_asiento.html', {'bus': bus, 'asiento': asiento})