"""
Configuración de URLs para la aplicación totalisting.

Este archivo define todas las rutas (endpoints) de la API relacionadas con:
- Productos (crear, leer, actualizar, eliminar)
- Categorías (crear, leer, actualizar, eliminar)
- Licencias (crear, leer, actualizar, eliminar)

Todas las rutas están organizadas por operación CRUD (Create, Read, Update, Delete)
y se incluyen en el proyecto principal mediante Ecommerce/urls.py.
"""

# Importar path de Django para definir rutas URL
from django.urls import path
# Importar todas las vistas de este módulo
from . import views

# Lista de patrones de URL para la aplicación totalisting
# Cada path define una ruta que mapea a una vista específica
urlpatterns = [
    # ========================================================================
    # CREATE - Rutas para crear nuevos registros
    # ========================================================================
    # Ruta para crear un nuevo producto
    # POST /product/create/
    path('product/create/', views.new_product_in_DB, name='new_product_in_DB'),
    
    # Ruta para crear una nueva categoría
    # POST /category/create/
    path('category/create/', views.create_category, name='create_category'),
    
    # Ruta para crear una nueva licencia
    # POST /licence/create/
    path('licence/create/', views.create_licence, name='create_licence'),
    
    # ========================================================================
    # READ - Rutas para leer/consultar registros
    # ========================================================================
    
    # --- Rutas de Categorías ---
    # Ruta para listar todas las categorías
    # GET /category/
    path('category/', views.listing, name='listing'),
    
    # Ruta para listar categorías filtradas por licencia
    # GET /category/by-license/<nombre_licencia>/
    # Ejemplo: /category/by-license/star-wars/
    path('category/by-license/<str:license_name>/', views.category_list_by_license, name='category_list_by_license'),
    
    # Ruta para obtener información de una categoría específica
    # GET /category/<nombre_categoria>/
    path('category/<str:category_name>/', views.category, name='category'),
    
    # --- Rutas de Licencias ---
    # Ruta para listar todas las licencias
    # GET /licence/
    path('licence/', views.license_view, name='licence'),
    
    # Ruta para obtener información de una licencia específica
    # GET /licence/<nombre_licencia>/
    path('licence/<str:license_name>/', views.license, name='license'),
    
    # --- Rutas de Productos - Listados ---
    # Ruta para listar todos los productos
    # GET /product/list/
    path('product/list/', views.product_list, name='product_list'),
    
    # Ruta para listar productos filtrados por categoría
    # GET /product/list/category/<nombre_categoria>/
    # Ejemplo: /product/list/category/figuras/
    path('product/list/category/<str:category_name>/', views.product_list_by_category, name='product_list_by_category'),
    
    # Ruta para listar productos filtrados por licencia
    # GET /product/list/license/<nombre_licencia>/
    # Ejemplo: /product/list/license/star-wars/
    path('product/list/license/<str:license_name>/', views.product_list_by_license, name='product_list_by_license'),
    
    # Ruta para obtener información de un producto por nombre
    # GET /product/<nombre_producto>/
    path('product/<str:product_name>/', views.product, name='product'),
    
    # --- Rutas de Productos - Búsquedas específicas ---
    # Ruta para buscar un producto por su ID único
    # GET /product/find/id/<id_producto>/
    # Ejemplo: /product/find/id/1/
    path('product/find/id/<int:product_id>/', views.find_product_by_id, name='find_product_by_id'),
    
    # Ruta para buscar un producto por su nombre exacto
    # GET /product/find/name/<nombre_producto>/
    # Ejemplo: /product/find/name/baby-yoda-blueball/
    path('product/find/name/<str:product_name>/', views.find_product_by_name, name='find_product_by_name'),
    
    # Ruta para buscar un producto por su SKU (código único)
    # GET /product/find/sku/<sku>/
    # Ejemplo: /product/find/sku/STW001001/
    path('product/find/sku/<str:sku>/', views.find_product_by_sku, name='find_product_by_sku'),
    
    # ========================================================================
    # UPDATE - Rutas para actualizar registros
    # ========================================================================
    # Ruta para actualizar un producto existente
    # POST/PUT /product/update/<id_producto>/
    # Ejemplo: /product/update/1/
    path('product/update/<int:product_id>/', views.update_product, name='update_product'),
    
    # Ruta para actualizar una categoría existente
    # POST/PUT /category/update/<id_categoria>/
    path('category/update/<int:category_id>/', views.update_category, name='update_category'),
    
    # Ruta para actualizar una licencia existente
    # POST/PUT /licence/update/<id_licencia>/
    path('licence/update/<int:licence_id>/', views.update_licence, name='update_licence'),
    
    # ========================================================================
    # DELETE - Rutas para eliminar registros
    # ========================================================================
    # Ruta para eliminar un producto
    # DELETE /product/delete/<id_producto>/
    # Ejemplo: /product/delete/1/
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    
    # Ruta para eliminar una categoría
    # DELETE /category/delete/<id_categoria>/
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
    # Ruta para eliminar una licencia
    # DELETE /licence/delete/<id_licencia>/
    path('licence/delete/<int:licence_id>/', views.delete_licence, name='delete_licence'),
]