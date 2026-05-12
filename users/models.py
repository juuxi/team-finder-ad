from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .constants import (
    USER_NAME_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_ABOUT_MAX_LENGTH,
)


class UserManager(BaseUserManager):

    def create_user(self, email, name, surname, avatar, phone, password=None):
        """
        Создание пользователя по переданным email, имени, фамилии, аватару
        и номеру телефона
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            surname=surname,
            avatar=avatar,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, avatar, phone, password=None):
        """
        Создание суперпользователя по переданным email, имени, фамилии, аватару
        и номеру телефона
        """
        user = self.create_user(
            email=email,
            name=name,
            surname=surname,
            avatar=avatar,
            phone=phone,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )

    name = models.CharField(max_length=USER_NAME_MAX_LENGTH, verbose_name='Имя')

    surname = models.CharField(
        max_length=USER_SURNAME_MAX_LENGTH, verbose_name='Фамилия'
    )

    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватарка')

    phone = models.CharField(
        max_length=USER_PHONE_MAX_LENGTH, verbose_name='Номер телефона'
    )

    github_url = models.URLField(null=True, blank=True, verbose_name='Ссылка на github')

    about = models.TextField(
        max_length=USER_ABOUT_MAX_LENGTH, null=True, blank=True, verbose_name='Описание'
    )

    favorites = models.ManyToManyField(
        'projects.Project',
        blank=True,
        related_name='interested_users',
        verbose_name='Избранные проекты',
    )

    is_active = models.BooleanField(default=True, verbose_name='Активен')

    is_staff = models.BooleanField(default=False, verbose_name='Администратор')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'avatar', 'phone']

    def __str__(self):
        return self.email
