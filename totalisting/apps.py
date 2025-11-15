from django.apps import AppConfig


class TotalistingConfig(AppConfig):
    """
    Configuración de la aplicación Totalisting.
    
    Esta aplicación maneja el listado y visualización de productos
    en el sistema de comercio electrónico.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'totalisting'
