from .models import Bus, Ruta, Cliente
from django import forms
from .models import Disponibilidad

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'rut', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DisponibilidadForm(forms.ModelForm):
    horas = (    ('06:00', '06:00'),    ('07:00', '07:00'),    ('08:00', '08:00'),    ('09:00', '09:00'),    ('10:00', '10:00'),    ('11:00', '11:00'),    ('12:00', '12:00'),    ('13:00', '13:00'),    ('14:00', '14:00'),    ('15:00', '15:00'),    ('16:00', '16:00'),    ('17:00', '17:00'),    ('18:00', '18:00'),    ('19:00', '19:00'),    ('20:00', '20:00'),    ('21:00', '21:00'),    ('22:00', '22:00'),    ('23:00', '23:00'),)
    horario=forms.ChoiceField(choices=horas)
    class Meta:
        model = Disponibilidad
        fields = ['bus', 'ruta', 'fecha', 'horario', 'disponible']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'ruta': forms.Select(attrs={'class': 'form-control'}, choices=[(ruta.id, str(ruta)) for ruta in Ruta.objects.all()]),
        }
        input_formats = ['%d-%m-%Y']  # Añade el formato de fecha para que pueda interpretar correctamente la fecha

class BusquedaRutasForm(forms.Form):
    origen = forms.CharField(max_length=100)
    destino = forms.CharField(max_length=100)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class BusForm(forms.ModelForm):

    class Meta:
        model = Bus
        fields = ('patente','cantidadAsientos')

class RutaForm(forms.ModelForm):
    
    Opciones=(
        ('Talca', 'Talca'),
        ('Curicó', 'Curicó'),
        ('Maule', 'Maule'),
        ('Linares', 'Linares'),
    )
    origen = forms.ChoiceField(choices=Opciones)
    destino = forms.ChoiceField(choices=Opciones)
    class Meta:
        model = Ruta
        fields = ('origen', 'destino', 'tiempoEstimado')

class CliForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ('nombre', 'apellido', 'email')