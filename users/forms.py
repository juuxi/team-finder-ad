from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

from .utils import handle_clean_phone, handle_clean_github_url

User = get_user_model()


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'surname', 'email']


class AdminUserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'surname', 'email']


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['avatar', 'name', 'surname', 'about', 'phone', 'github_url']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return handle_clean_phone(phone, self.instance)

    def clean_github_url(self):
        github_url = self.cleaned_data['github_url']
        return handle_clean_github_url(github_url)


class UserChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = []

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not check_password(old_password, self.request.user.password):
            raise ValidationError("Пароль неверный")
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2
