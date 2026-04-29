from django.shortcuts import render

def list(request):
    template = 'projects/project_list.html'
    return render(request, template)
