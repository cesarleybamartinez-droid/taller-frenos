from django.core.management.base import BaseCommand
from inventario.models import CategoriaRepuesto

class Command(BaseCommand):
    help = 'Carga las categorías iniciales de repuestos'

    def handle(self, *args, **options):
        categorias = [
            'Pastillas',
            'Discos',
            'Tambores',
            'Líquido de frenos',
            'Sensores',
            'Herramientas',
            'Otros',
        ]
        for nombre in categorias:
            cat, created = CategoriaRepuesto.objects.get_or_create(nombre=nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoría "{nombre}" creada'))
            else:
                self.stdout.write(f'Categoría "{nombre}" ya existe')