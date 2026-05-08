from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http import HttpResponseForbidden

from .models import Project


class ProjectListView(ListView):
    model = Project
    ordering = ('-created_at')
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


class FavoritesListView(LoginRequiredMixin, ListView):
    template_name = 'projects/favorite_projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return self.request.user.favorites.all()


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'
    template_name = 'projects/project-details.html'


@login_required
def complete_project(request, project_id=None):
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    if project.owner == user and project.status == 'open':
        project.status = 'closed'
        project.save()
        return JsonResponse({'status': 'ok', 'project_status': 'closed'})
    return HttpResponseForbidden()


@login_required
def toggle_participate(request, project_id=None):
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    if user in project.participants.all():
        project.participants.remove(user)
        return JsonResponse({'status': 'ok', 'participant': False})

    project.participants.add(user)
    return JsonResponse({'status': 'ok', 'participant': True})
