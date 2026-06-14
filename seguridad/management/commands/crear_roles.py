from django.core.management.base import BaseCommand
from seguridad.models import Rol, Permiso, RolPermiso

class Command(BaseCommand):
    help = 'Crea los roles, los permisos y los asigna'

    def handle(self, *args, **options):
        # 1. Roles
        nombres_roles = ['Propietario', 'Administrador', 'Recepcionista']
        roles = {}
        for nombre in nombres_roles:
            rol, _ = Rol.objects.get_or_create(nombre=nombre)
            roles[nombre] = rol

        # 2. Permisos
        nombres_permisos = [
            'crear_usuario',
            'editar_usuario',
            'desactivar_usuario',
            'ver_auditoria',
            'gestionar_inventario',
            'gestionar_compras',
            'ver_finanzas',
            'gestionar_finanzas',
            'ver_reportes',
            'anular_orden',
            'cambiar_estado_orden',
            'ver_dashboard_financiero',
            'gestionar_permisos',
        ]
        permisos = {}
        for nombre in nombres_permisos:
            permiso, _ = Permiso.objects.get_or_create(nombre=nombre)
            permisos[nombre] = permiso

        # 3. Asignación de permisos a roles
        asignaciones = {
            'Propietario': nombres_permisos,  # todos los permisos
            'Administrador': [
                'gestionar_inventario',
                'gestionar_compras',
                'ver_finanzas',
                'gestionar_finanzas',
                'ver_reportes',
                'cambiar_estado_orden',
                'ver_dashboard_financiero',
                'desactivar_usuario',
                
            ],
            'Recepcionista': []  # sus limitaciones se manejan directamente en las vistas
        }

        for rol_nombre, lista_permisos in asignaciones.items():
            rol = roles[rol_nombre]
            for codigo in lista_permisos:
                permiso = permisos[codigo]
                _, created = RolPermiso.objects.get_or_create(rol=rol, permiso=permiso)
                if created:
                    self.stdout.write(f'Permiso "{codigo}" asignado a {rol_nombre}')

        self.stdout.write(self.style.SUCCESS('Roles y permisos actualizados'))