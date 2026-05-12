from django import forms

from .models import Project
from .utils import handle_clean_github_url


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']

    def clean_github_url(self):
        github_url = self.cleaned_data['github_url']
        return handle_clean_github_url(github_url)
