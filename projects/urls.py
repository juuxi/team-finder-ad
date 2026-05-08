from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.ProjectListView.as_view(), name='list'),
    path('<int:project_id>/toggle-favorite/', views.toggle_favorite,
         name='toggle-favorite'),
]
