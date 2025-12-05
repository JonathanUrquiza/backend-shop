#!/usr/bin/env python
"""
Utilidad de línea de comandos de Django para tareas administrativas.

Este archivo es el punto de entrada para ejecutar comandos de Django desde la terminal.
Permite ejecutar comandos como:
- python manage.py runserver (iniciar servidor de desarrollo)
- python manage.py migrate (aplicar migraciones)
- python manage.py createsuperuser (crear usuario administrador)
- python manage.py shell (abrir shell de Django)
- etc.

Para más información sobre comandos disponibles:
https://docs.djangoproject.com/en/5.2/ref/django-admin/
"""

# Importar módulo os para variables de entorno
import os
# Importar módulo sys para argumentos de línea de comandos
import sys


def main():
    """
    Ejecutar tareas administrativas de Django.
    
    Esta función configura Django y ejecuta comandos desde la línea de comandos.
    Se ejecuta cuando se llama a 'python manage.py <comando>'.
    
    Configuración:
    - Establece DJANGO_SETTINGS_MODULE para que Django sepa dónde está la configuración
    - Ejecuta el comando solicitado desde sys.argv
    """
    # Establecer el módulo de configuración de Django por defecto
    # Django necesita saber dónde está el archivo settings.py
    # 'Ecommerce.settings' significa: módulo 'settings' dentro del paquete 'Ecommerce'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')
    
    try:
        # Importar la función execute_from_command_line de Django
        # Esta función procesa los argumentos de línea de comandos y ejecuta el comando
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si no se puede importar Django, lanzar error con mensaje útil
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado y "
            "disponible en tu variable de entorno PYTHONPATH? ¿Olvidaste "
            "activar un entorno virtual?"
        ) from exc
    
    # Ejecutar el comando de Django con los argumentos de la línea de comandos
    # sys.argv contiene los argumentos pasados al script
    # Ejemplo: ['manage.py', 'runserver'] -> ejecuta el servidor de desarrollo
    execute_from_command_line(sys.argv)


# Ejecutar main() solo si este archivo se ejecuta directamente (no si se importa)
if __name__ == '__main__':
    main()
