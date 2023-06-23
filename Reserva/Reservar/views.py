from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404

from .models import Bus, Ruta, Cliente
##from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import BusForm, RutaForm, CliForm



@login_required
def index(request):
    return render(request, 'index.html')

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
        return redirect('/buses')

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
        return redirect('/rutas')
    contexto = {
        'ruta': ruta,
    }
    return render(request, 'rutas/del_rutas.html', contexto)
