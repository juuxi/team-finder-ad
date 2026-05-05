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


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'surname', 'email']
