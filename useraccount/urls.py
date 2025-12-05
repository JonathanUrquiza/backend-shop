from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.user_profile_edit, name='user_profile_edit'),
    path('profile/delete/', views.user_profile_delete, name='user_profile_delete'),
    path('profile/change-password/', views.user_profile_change_password, name='user_profile_change_password'),
    path('profile/change-email/', views.user_profile_change_email, name='user_profile_change_email'),
    path('profile/change-username/', views.user_profile_change_username, name='user_profile_change_username'),
    path('profile/change-avatar/', views.user_profile_change_avatar, name='user_profile_change_avatar'),
    path('profile/change-background/', views.user_profile_change_background, name='user_profile_change_background'),
    path('profile/change-theme/', views.user_profile_change_theme, name='user_profile_change_theme'),
    path('profile/change-language/', views.user_profile_change_language, name='user_profile_change_language'),
    # CRUD de usuarios (solo admin)
    path('list/', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('update/<int:user_id>/', views.user_update, name='user_update'),
    path('delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('roles/', views.role_list, name='role_list'),
]

