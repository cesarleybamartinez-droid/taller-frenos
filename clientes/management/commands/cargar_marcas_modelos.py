from django.core.management.base import BaseCommand
from clientes.models import Marca, ModeloVehiculo

class Command(BaseCommand):
    help = 'Carga marcas y modelos de vehículos comunes'

    def handle(self, *args, **options):
        datos = {
            'Toyota': ['Corolla', 'Yaris', 'Hilux', 'RAV4', 'Camry'],
            'Honda': ['Civic', 'CR-V', 'Fit', 'Pilot'],
            'Nissan': ['Sentra', 'Versa', 'X-Trail', 'Kicks'],
            'Hyundai': ['Elantra', 'Tucson', 'Santa Fe', 'Accent'],
            'Kia': ['Rio', 'Sportage', 'Seltos'],
            'Mitsubishi': ['Lancer', 'Montero', 'Outlander'],
            'Ford': ['Focus', 'Escape', 'Ranger'],
            'Chevrolet': ['Cruze', 'Spark', 'Tracker'],
            'Volkswagen': ['Jetta', 'Golf', 'Tiguan'],
            'Suzuki': ['Swift', 'Vitara', 'Jimny'],
        }
        for nombre_marca, modelos in datos.items():
            marca, created = Marca.objects.get_or_create(nombre=nombre_marca)
            if created:
                self.stdout.write(f'Marca "{nombre_marca}" creada')
            for nombre_modelo in modelos:
                modelo, created = ModeloVehiculo.objects.get_or_create(
                    marca=marca, nombre=nombre_modelo
                )
                if created:
                    self.stdout.write(f'  Modelo "{nombre_modelo}" creado')
        self.stdout.write(self.style.SUCCESS('Catálogo de marcas y modelos cargado.'))