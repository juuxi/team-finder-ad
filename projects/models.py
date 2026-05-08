from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Владелец'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    github_url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Ссылка на github'
    )

    STATUS_OPTIONS = [
        ('open', 'Open'),
        ('closed', 'Closed')
    ]

    status = models.CharField(
        max_length=6,
        choices=STATUS_OPTIONS,
        verbose_name='Статус'
    )

    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники'
    )

    def __str__(self):
        return self.name
