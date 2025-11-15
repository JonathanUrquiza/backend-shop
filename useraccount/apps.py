from django.apps import AppConfig


class UseraccountConfig(AppConfig):
    """
    Configuración de la aplicación Useraccount.
    
    Esta aplicación maneja las cuentas de usuario, autenticación
    y gestión de perfiles en el sistema de comercio electrónico.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'useraccount'
