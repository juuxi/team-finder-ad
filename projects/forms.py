from django import forms

from django.core.exceptions import ValidationError

from .models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']

    def clean_github_url(self):
        github_url = self.cleaned_data['github_url']
        github_url = github_url.lower()
        website_part = github_url.split('://', 1)[-1]
        if not website_part.startswith('github.com'):
            raise ValidationError('Ссылка должна вести на github')

        return github_url
