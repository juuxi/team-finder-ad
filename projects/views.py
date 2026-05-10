from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http import HttpResponseForbidden

from .models import Project
from .forms import ProjectForm


class ProjectListView(ListView):
    model = Project
    ordering = ('-created_at')
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12


@require_http_methods(["POST"])
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


@require_http_methods(["POST"])
@login_required
def complete_project(request, project_id=None):
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    if project.owner == user:
        if project.status == 'open':
            project.status = 'closed'
            project.save()
            return JsonResponse({'status': 'ok', 'project_status': 'closed'})
        return JsonResponse({'status': 'error', 'project_status': 'closed'})
    return HttpResponseForbidden()


@require_http_methods(["POST"])
@login_required
def toggle_participate(request, project_id=None):
    user = request.user
    project = get_object_or_404(Project, pk=project_id)
    if user in project.participants.all():
        project.participants.remove(user)
        return JsonResponse({'status': 'ok', 'participant': False})

    project.participants.add(user)
    return JsonResponse({'status': 'ok', 'participant': True})


@login_required
def create_update_project(request, project_id=None):
    instance = None
    is_edit = False
    if project_id:
        instance = get_object_or_404(Project, pk=project_id)
        is_edit = True
    form = ProjectForm(request.POST or None, instance=instance)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect('projects:project-details', project_id=project.id)
    context = {'form': form, 'is_edit': is_edit}
    return render(request, 'projects/create-project.html', context)
