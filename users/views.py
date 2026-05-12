from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django_filters.views import FilterView

from . import forms
from .filters import UserFilter
from .constants import PAGINATE_BY
from .utils import assign_user_avatar

User = get_user_model()


@login_required
def logout_view(request):
    logout(request)

    return redirect('/projects/list/')


def login_view(request):
    form = forms.UserLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/projects/list/')
            form.add_error(None, 'Неверный имейл или пароль')
    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    form = forms.UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data['password']
            user.set_password(password)
            assign_user_avatar(user)
            user.save()
            if user is not None:
                login(request, user)
                return redirect('/projects/list/')
    return render(request, 'users/register.html', {'form': form})


@login_required
def edit_profile_view(request):
    form = forms.UserChangeForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(f'/users/{request.user.id}/')
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    form = forms.UserChangePasswordForm(request.POST or None, request=request)
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password2'])
            user.save()
            if user is not None:
                login(request, user)
                return redirect(f'/users/{request.user.id}/')
    return render(request, 'users/change_password.html', {'form': form})


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'
    template_name = 'users/user-details.html'


class UserListFilterView(FilterView):
    model = User
    filterset_class = UserFilter
    context_object_name = 'participants'
    template_name = 'users/participants.html'
    ordering = 'id'
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_param = self.request.GET.get('filter')

        context['active_filter'] = filter_param

        return context

    # игнорирование параметра фильтрации для
    # неаутентифицированных пользователей
    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)

        if not self.request.user.is_authenticated:
            kwargs['data'] = None
        return kwargs
