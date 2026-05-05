from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def handle_logout(request):
    """
    Кастомная обработка logout-а
    """
    logout(request)

    return redirect('/projects/list/')
