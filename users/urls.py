from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('edit-profile/', views.edit_profile_view, name='edit-profile'),
    path('change-password/', views.change_password_view,
         name='change-password'),
]
