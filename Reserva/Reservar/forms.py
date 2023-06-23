from django import forms
from .models import Bus, Ruta, Cliente

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