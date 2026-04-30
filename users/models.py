from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )

    name = models.CharField(
        max_length=124,
        verbose_name='Имя'
    )

    surname = models.CharField(
        max_length=124,
        verbose_name='Фамилия'
    )

    avatar = models.ImageField(
        verbose_name='Аватарка'
    )

    phone = models.CharField(
        max_length=12,
        verbose_name='Номер телефона'
    )

    github_url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Ссылка на github'
    )

    about = models.TextField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name='Администратор'
    )

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
