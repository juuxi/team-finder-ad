from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.ProjectListView.as_view(), name='list'),
    path(
        '<int:project_id>/toggle-favorite/',
        views.toggle_favorite,
        name='toggle-favorite',
    ),
    path('favorites/', views.FavoritesListView.as_view(), name='favorites'),
    path(
        '<int:project_id>/', views.ProjectDetailView.as_view(), name='project-details'
    ),
    path('<int:project_id>/complete/', views.complete_project, name='complete'),
    path(
        '<int:project_id>/toggle-participate/',
        views.toggle_participate,
        name='toggle-participate',
    ),
    path('create-project/', views.create_update_project, name='create-project'),
    path('<int:project_id>/edit/', views.create_update_project, name='edit-project'),
]
