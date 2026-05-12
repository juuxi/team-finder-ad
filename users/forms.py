from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

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
        if (not phone.startswith('8')) and (not phone.startswith('+7')):
            raise ValidationError('Формат номера телефона - 8XXXXXXXXXX  или \
                                  +7XXXXXXXXXX')
        if phone.startswith('8'):
            phone = phone.replace('8', '+7', 1)

        if len(phone) != 12:
            raise ValidationError('Формат номера телефона - 8XXXXXXXXXX  или \
                                  +7XXXXXXXXXX')

        if (not phone == self.instance.phone) and (
            User.objects.filter(phone=phone).exists()
        ):
            raise ValidationError('Пользователь с таким номером \
            телефона уже существует')

        return phone

    def clean_github_url(self):
        github_url = self.cleaned_data['github_url']
        if not github_url:
            return None
        github_url = github_url.lower()
        website_part = github_url.split('://', 1)[-1]
        if not website_part.startswith('github.com'):
            raise ValidationError('Ссылка должна вести на github')

        return github_url


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
