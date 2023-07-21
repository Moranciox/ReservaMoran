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
from django.db import IntegrityError
from datetime import date

def about_us(request):
    # Puedes agregar cualquier información que desees mostrar en la página "Acerca de nosotros"
    context = {
        'titulo': 'Acerca de Nosotros',
        'contenido': 'Somos una empresa ficticia dedicada a ofrecer servicios de transporte de alta calidad. Nuestro equipo está comprometido con brindar la mejor experiencia de viaje a nuestros clientes.',
    }
    return render(request, 'about_us.html', context)

def viajes_disponibles(request):
    # Obtener los viajes disponibles para el día de hoy
    viajes_hoy = Disponibilidad.objects.filter(fecha=date.today())

    # Renderizar la plantilla con la lista de viajes disponibles
    return render(request, 'viajes_disponibles.html', {'viajes_hoy': viajes_hoy})


@login_required
def lista_reservas_cliente(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    reservas = Reserva.objects.filter(cliente=cliente)
    context = {
        'cliente': cliente,
        'reservas': reservas,
    }
    return render(request, 'Clientes/lista_reservas_cliente.html', context)

def reserva_pasaje(request, disponibilidad_id):
    disponibilidad = get_object_or_404(Disponibilidad, id=disponibilidad_id)
    asientos_disponibles = Asientos.objects.filter(
        bus=disponibilidad.bus,
        estado=True,
        disponibilidad__fecha=disponibilidad.fecha,
        disponibilidad__horario=disponibilidad.horario
    )

    if request.method == 'POST':
        asientos_seleccionados = request.POST.getlist('asientos')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        rut = request.POST.get('rut')
        telefono = request.POST.get('telefono')

        # Verificar si el cliente ya existe en la base de datos
        try:
            cliente = Cliente.objects.get(email=email, rut=rut)
            # Si el cliente ya existe, actualizamos sus datos con lo ingresado en el formulario
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.telefono = telefono
            cliente.save()
        except Cliente.DoesNotExist:
            # Si el cliente no existe, lo creamos
            cliente = Cliente.objects.create(nombre=nombre, apellido=apellido, email=email, rut=rut, telefono=telefono)

        # Crear y guardar el registro de reserva con las fechas correctas
        reserva = Reserva(
            fechaReserva=datetime.combine(disponibilidad.fecha, disponibilidad.horario),  # Fecha y hora de la disponibilidad
            fechaCreacion=timezone.now(),  # Fecha de creación de la reserva (fecha actual)
            cantidadPasajes=len(asientos_seleccionados),  # Cantidad de asientos seleccionados
            cliente=cliente,
            ruta=disponibilidad.ruta,
            bus=disponibilidad.bus,
        )
        reserva.save()

        # Asignar los asientos seleccionados a la reserva y marcarlos como no disponibles
        asientos_reserva = []
        for asiento_numero in asientos_seleccionados:
            # Utilizamos filter() en lugar de get()
            asientos = Asientos.objects.filter(bus=disponibilidad.bus, numero=asiento_numero, estado=True)
            if asientos.exists():
                asiento = asientos.first()  # Tomamos el primer asiento disponible de los que coinciden
                asiento.estado = False
                asiento.save()
                asientos_reserva.append(asiento)

        # Guardar los asientos seleccionados en la reserva
        for asiento in asientos_reserva:
            reserva.asientos.add(asiento)

        # Marcar la disponibilidad como no disponible
        disponibilidad.disponible = False
        disponibilidad.save()

        # Redirigir a una página de confirmación o a donde desees
        return render(request, 'cliente/confirmacion_reserva.html', {'disponibilidad': disponibilidad, 'cliente': cliente, 'reserva': reserva})

    contexto = {
        'disponibilidad': disponibilidad,
        'asientos_disponibles': asientos_disponibles,
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

@login_required
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

@login_required
def del_disponibilidad(request, pk):
    disponibilidad = get_object_or_404(Disponibilidad, pk=pk)

    if request.method == 'POST':
        disponibilidad.delete()
        return redirect('list_disponibilidad')

    context = {
        'disponibilidad': disponibilidad,
    }
    return render(request, 'disponibilidad/del_disponibilidad.html', context)

@login_required
def list_asientos(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    asientos = bus.asientos.all()
    return render(request, 'asiento/list_asientos.html', {'bus': bus, 'asientos': asientos})

@login_required
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

@login_required
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

@login_required
def del_asiento(request, bus_id, asiento_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    asiento = get_object_or_404(Asiento, pk=asiento_id)

    if request.method == 'POST':
        asiento.delete()
        return redirect('list_asientos', bus_id=bus_id)

    return render(request, 'asiento/del_asiento.html', {'bus': bus, 'asiento': asiento})