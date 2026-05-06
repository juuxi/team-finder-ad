from django import forms

from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError

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


class UserEditProfileForm(forms.ModelForm):

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

        if ((not phone == self.instance.phone)
           and (User.objects.filter(phone=phone).exists())):
            raise ValidationError('Пользователем с таким номером \
            телефона уже существует')

        return phone

    def clean_github_url(self):
        github_url = self.cleaned_data['github_url']
        github_url = github_url.lower()
        website_part = github_url.split('://', 1)[-1]
        if not website_part.startswith('github.com'):
            raise ValidationError('Ссылка должна вести на github')

        return github_url
