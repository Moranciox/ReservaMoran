from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    apellido = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=False, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    rut = models.CharField(max_length=200, null=False, unique=True)

    def __str__(self):
        return self.nombre

class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    tiempoEstimado = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.origen} - {self.destino}"
        
class Bus(models.Model):
    patente=models.CharField(max_length=50, unique=True)
    cantidadAsientos = models.IntegerField()

    def __str__(self):
        return self.patente

class Disponibilidad(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='disponibilidades_bus')
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name='disponibilidades_ruta')
    horario = models.TimeField()
    fecha = models.DateField()
    disponible = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.ruta} - {self.fecha} - {self.horario}"

class Asientos(models.Model):
    numero = models.IntegerField(blank=True, null=True)
    estado = models.BooleanField(default=False)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    disponibilidad = models.ForeignKey(Disponibilidad, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.numero)



from django.utils import timezone

class Reserva(models.Model):
    fechaReserva = models.DateTimeField(null=False)
    fechaCreacion = models.DateTimeField(default=timezone.now)  # Agregar el atributo fechaCreacion
    cantidadPasajes = models.IntegerField(null=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    asiento = models.ForeignKey(Asientos, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reserva de {self.cliente} - Fecha de Reserva: {self.fechaReserva}"

@receiver(post_save, sender=Disponibilidad)
def crear_asientos(sender, instance, created, **kwargs):
    if created:
        bus = instance.bus
        asientos = []
        for numero_asiento in range(1, bus.cantidadAsientos + 1):
            asiento = Asientos(numero=numero_asiento, estado=True, bus=bus, disponibilidad=instance)
            asientos.append(asiento)
        Asientos.objects.bulk_create(asientos)


# Create your models here.
