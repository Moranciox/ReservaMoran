# Generated by Django 4.2.1 on 2023-07-21 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservar', '0006_remove_disponibilidad_asiento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='asiento',
        ),
        migrations.AddField(
            model_name='reserva',
            name='asientos',
            field=models.ManyToManyField(to='Reservar.asientos'),
        ),
    ]
