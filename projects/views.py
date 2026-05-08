from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'


@login_required
def toggle_favorite(request, project_id=None):
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    if project in user.favorites.all():
        user.favorites.remove(project)
        return JsonResponse({'status': 'ok', 'favorited': False})

    user.favorites.add(project)
    return JsonResponse({'status': 'ok', 'favorited': True})
