from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import logout, login
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods

from . import forms


@require_http_methods(["GET"])
def handle_logout(request):
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
    return render(request, 'users/login.html', {'form': form})
