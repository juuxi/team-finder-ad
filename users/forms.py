from django import forms

from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'surname', 'email']


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['avatar', 'name', 'surname', 'about', 'phone', 'github_url']
