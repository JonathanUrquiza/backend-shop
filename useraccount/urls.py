"""
Configuración de URLs para la aplicación useraccount.

Este archivo define todas las rutas (endpoints) de la API relacionadas con:
- Autenticación de usuarios (login, logout, registro)
- Perfil de usuario (ver, editar, eliminar)
- Configuración de perfil (cambiar contraseña, email, avatar, etc.)
- CRUD de usuarios (solo para administradores)
- Gestión de roles

Todas las rutas están prefijadas con 'useraccount/' en el proyecto principal.
"""

# Importar path de Django para definir rutas URL
from django.urls import path
# Importar todas las vistas de este módulo
from . import views

# Lista de patrones de URL para la aplicación useraccount
# Cada path define una ruta que mapea a una vista específica
urlpatterns = [
    # ========================================================================
    # AUTENTICACIÓN - Rutas para login, registro y logout
    # ========================================================================
    # Ruta para iniciar sesión (login)
    # POST /useraccount/login/
    # Parámetros: email, password
    path('login/', views.user_login, name='user_login'),
    
    # Ruta para registrar un nuevo usuario
    # POST /useraccount/register/
    # Parámetros: name, lastname, email, password
    # Asigna automáticamente el rol "mixto" a nuevos usuarios
    path('register/', views.user_register, name='user_register'),
    
    # Ruta para cerrar sesión (logout)
    # POST /useraccount/logout/
    path('logout/', views.user_logout, name='user_logout'),
    
    # ========================================================================
    # PERFIL DE USUARIO - Rutas para gestionar el perfil del usuario
    # ========================================================================
    # Ruta para obtener información del perfil del usuario
    # GET /useraccount/profile/
    path('profile/', views.user_profile, name='user_profile'),
    
    # Ruta para editar el perfil del usuario
    # POST /useraccount/profile/edit/
    path('profile/edit/', views.user_profile_edit, name='user_profile_edit'),
    
    # Ruta para eliminar el perfil del usuario
    # POST /useraccount/profile/delete/
    path('profile/delete/', views.user_profile_delete, name='user_profile_delete'),
    
    # ========================================================================
    # CONFIGURACIÓN DE PERFIL - Rutas para cambiar configuraciones específicas
    # ========================================================================
    # Ruta para cambiar la contraseña del usuario
    # POST /useraccount/profile/change-password/
    path('profile/change-password/', views.user_profile_change_password, name='user_profile_change_password'),
    
    # Ruta para cambiar el email del usuario
    # POST /useraccount/profile/change-email/
    path('profile/change-email/', views.user_profile_change_email, name='user_profile_change_email'),
    
    # Ruta para cambiar el nombre de usuario
    # POST /useraccount/profile/change-username/
    path('profile/change-username/', views.user_profile_change_username, name='user_profile_change_username'),
    
    # Ruta para cambiar el avatar del usuario
    # POST /useraccount/profile/change-avatar/
    path('profile/change-avatar/', views.user_profile_change_avatar, name='user_profile_change_avatar'),
    
    # Ruta para cambiar el fondo de perfil del usuario
    # POST /useraccount/profile/change-background/
    path('profile/change-background/', views.user_profile_change_background, name='user_profile_change_background'),
    
    # Ruta para cambiar el tema del usuario (claro/oscuro)
    # POST /useraccount/profile/change-theme/
    path('profile/change-theme/', views.user_profile_change_theme, name='user_profile_change_theme'),
    
    # Ruta para cambiar el idioma del usuario
    # POST /useraccount/profile/change-language/
    path('profile/change-language/', views.user_profile_change_language, name='user_profile_change_language'),
    
    # ========================================================================
    # CRUD DE USUARIOS - Rutas para administradores (solo admin)
    # ========================================================================
    # Ruta para listar todos los usuarios (solo admin)
    # GET /useraccount/list/
    path('list/', views.user_list, name='user_list'),
    
    # Ruta para crear un nuevo usuario (solo admin)
    # POST /useraccount/create/
    # Parámetros: name, lastname, email, password, role_id (opcional)
    path('create/', views.user_create, name='user_create'),
    
    # Ruta para actualizar un usuario existente (solo admin)
    # PUT/POST /useraccount/update/<id_usuario>/
    # Ejemplo: /useraccount/update/1/
    path('update/<int:user_id>/', views.user_update, name='user_update'),
    
    # Ruta para eliminar un usuario (solo admin)
    # DELETE/POST /useraccount/delete/<id_usuario>/
    # Ejemplo: /useraccount/delete/1/
    path('delete/<int:user_id>/', views.user_delete, name='user_delete'),
    
    # Ruta para listar todos los roles disponibles
    # GET /useraccount/roles/
    # Útil para obtener la lista de roles al crear/editar usuarios
    path('roles/', views.role_list, name='role_list'),
]

