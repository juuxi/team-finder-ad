from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods

from . import forms


@require_http_methods(["GET"])
def logout_view(request):
    """
    Кастомная обработка logout-а
    """
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
            user.save()
            if user is not None:
                login(request, user)
                return redirect('/projects/list/')
    return render(request, 'users/register.html', {'form': form})


def edit_profile_view(request):
    form = forms.UserChangeForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/projects/list/')
    return render(request, 'users/edit_profile.html', {'form': form})


def change_password_view(request):
    form = forms.UserChangePasswordForm(request.POST or None, request=request)
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password2'])
            user.save()
            if user is not None:
                login(request, user)
                return redirect('/projects/list/')
    return render(request, 'users/change_password.html', {'form': form})
