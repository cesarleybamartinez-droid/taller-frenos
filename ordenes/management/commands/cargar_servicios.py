from django.core.management.base import BaseCommand
from ordenes.models import Servicio

class Command(BaseCommand):
    help = 'Carga los servicios iniciales del taller'

    def handle(self, *args, **options):
        servicios = [
            ('Diagnóstico de frenos', 'Revisión completa del sistema de frenos', 500.00),
            ('Cambio de pastillas delanteras', 'Sustitución de pastillas delanteras', 800.00),
            ('Cambio de pastillas traseras', 'Sustitución de pastillas traseras', 700.00),
            ('Cambio de discos delanteros', 'Sustitución de discos delanteros', 1,200.00),
            ('Cambio de discos traseros', 'Sustitución de discos traseros', 1,100.00),
            ('Cambio de tambores', 'Sustitución de tambores traseros', 1,500.00),
            ('Limpieza y ajuste de frenos', 'Mantenimiento preventivo', 600.00),
            ('Purga de líquido de frenos', 'Cambio y purga del sistema hidráulico', 900.00),
            ('Rectificación de discos', 'Rectificado de discos delanteros o traseros', 650.00),
            ('Cambio de sensores ABS', 'Sustitución de sensores', 400.00),
        ]
        for nombre, desc, precio in servicios:
            s, created = Servicio.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': desc, 'precio_estandar': precio}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Servicio "{nombre}" creado'))
            else:
                self.stdout.write(f'Servicio "{nombre}" ya existe')