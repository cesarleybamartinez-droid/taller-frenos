from django.core.management.base import BaseCommand
from seguridad.models import Rol

class Command(BaseCommand):
    help = 'Crea los roles iniciales del sistema (Propietario, Administrador, Recepcionista)'

    def handle(self, *args, **options):
        roles = ['Propietario', 'Administrador', 'Recepcionista']
        for nombre in roles:
            rol, created = Rol.objects.get_or_create(nombre=nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Rol "{nombre}" creado exitosamente'))
            else:
                self.stdout.write(f'Rol "{nombre}" ya existe')