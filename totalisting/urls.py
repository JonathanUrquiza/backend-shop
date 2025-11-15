from django.urls import path
from . import views

urlpatterns = [
    # ========================================================================
    # CREATE - Rutas para crear nuevos registros
    # ========================================================================
    path('product/create/', views.new_product_in_DB, name='new_product_in_DB'),
    
    # ========================================================================
    # READ - Rutas para leer/consultar registros
    # ========================================================================
    
    # Categorías
    path('category/', views.listing, name='listing'),
    path('category/by-license/<str:license_name>/', views.category_list_by_license, name='category_list_by_license'),
    path('category/<str:category_name>/', views.category, name='category'),
    
    # Licencias
    path('licence/', views.license_view, name='licence'),
    path('licence/<str:license_name>/', views.license, name='license'),
    
    # Productos - Listados
    path('product/list/', views.product_list, name='product_list'),
    path('product/list/category/<str:category_name>/', views.product_list_by_category, name='product_list_by_category'),
    path('product/list/license/<str:license_name>/', views.product_list_by_license, name='product_list_by_license'),
    path('product/<str:product_name>/', views.product, name='product'),
    
    # Productos - Búsquedas específicas
    path('product/find/id/<int:product_id>/', views.find_product_by_id, name='find_product_by_id'),
    path('product/find/name/<str:product_name>/', views.find_product_by_name, name='find_product_by_name'),
    path('product/find/sku/<str:sku>/', views.find_product_by_sku, name='find_product_by_sku'),
    
    # ========================================================================
    # UPDATE - Rutas para actualizar registros
    # ========================================================================
    path('product/update/<int:product_id>/', views.update_product, name='update_product'),
    path('category/update/<int:category_id>/', views.update_category, name='update_category'),
    path('licence/update/<int:licence_id>/', views.update_licence, name='update_licence'),
    
    # ========================================================================
    # DELETE - Rutas para eliminar registros
    # ========================================================================
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('licence/delete/<int:licence_id>/', views.delete_licence, name='delete_licence'),
]