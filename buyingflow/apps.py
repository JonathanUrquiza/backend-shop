from django.apps import AppConfig


class BuyingflowConfig(AppConfig):
    """
    Configuración de la aplicación Buyingflow.
    
    Esta aplicación maneja el flujo de compra y procesamiento
    de pedidos en el sistema de comercio electrónico.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buyingflow'
