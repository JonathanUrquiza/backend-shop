"""
Configuración de URLs principal para el proyecto Ecommerce.

Este archivo es el punto de entrada para todas las URLs del proyecto Django.
Define cómo se enrutan las peticiones HTTP a las diferentes aplicaciones.

La lista `urlpatterns` enruta las URLs a las vistas. Para más información ver:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

Ejemplos de uso:
Vistas basadas en funciones:
    1. Agregar una importación:  from my_app import views
    2. Agregar una URL a urlpatterns:  path('', views.home, name='home')

Vistas basadas en clases:
    1. Agregar una importación:  from other_app.views import Home
    2. Agregar una URL a urlpatterns:  path('', Home.as_view(), name='home')

Incluir otra URLconf:
    1. Importar la función include(): from django.urls import include, path
    2. Agregar una URL a urlpatterns:  path('blog/', include('blog.urls'))
"""

# Importar admin de Django para el panel de administración
from django.contrib import admin
# Importar path e include para definir rutas y incluir otras configuraciones de URL
from django.urls import path, include


# Lista de patrones de URL principales del proyecto
# Django procesa estos patrones en orden, deteniéndose en el primero que coincida
urlpatterns = [
    # Incluir todas las URLs de la aplicación totalisting (productos, categorías, licencias)
    # Las rutas de totalisting estarán disponibles directamente en la raíz
    # Ejemplo: /product/list/, /category/, /licence/
    path('', include('totalisting.urls')),
    
    # Panel de administración de Django
    # Disponible en /admin/
    # Permite gestionar modelos desde la interfaz web de Django
    path('admin/', admin.site.urls),
    
    # Incluir todas las URLs de la aplicación useraccount (autenticación, usuarios)
    # Las rutas de useraccount estarán prefijadas con 'useraccount/'
    # Ejemplo: /useraccount/login/, /useraccount/register/, /useraccount/list/
    path('useraccount/', include('useraccount.urls')),
    
    # Ruta comentada para la aplicación buyingflow (flujo de compras)
    # Se puede descomentar cuando se implemente la funcionalidad de compras
    # path('buy/', include('buyingflow.urls')),
]
