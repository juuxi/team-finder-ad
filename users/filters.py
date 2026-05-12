import django_filters
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    OWNERS_OF_FAVORITE_PROJECTS_NAME = 'owners-of-favorite-projects'
    OWNERS_OF_PARTICIPATING_PROJECTS = 'owners-of-participating-projects'
    INTERSETED_IN_MY_PROJECTS = 'interested-in-my-projects'
    PARTICIPANTS_OF_MY_PROJECTS = 'participants-of-my-projects'

    owners_of_favorite_projects = django_filters.CharFilter(
        method='filter_owners_of_favorite_projects',
        widget=forms.CheckboxInput(attrs={'name': OWNERS_OF_FAVORITE_PROJECTS_NAME}),
    )

    owners_of_participating_projects = django_filters.CharFilter(
        method='filter_owners_of_participating_projects',
        widget=forms.CheckboxInput(attrs={'name': OWNERS_OF_PARTICIPATING_PROJECTS}),
    )

    interested_in_my_projects = django_filters.CharFilter(
        method='filter_interested_in_my_projects',
        widget=forms.CheckboxInput(attrs={'name': INTERSETED_IN_MY_PROJECTS}),
    )

    participants_of_my_projects = django_filters.CharFilter(
        method='filter_participants_of_my_projects',
        widget=forms.CheckboxInput(attrs={'name': PARTICIPANTS_OF_MY_PROJECTS}),
    )

    class Meta:
        model = User
        fields = []

    def filter_owners_of_favorite_projects(self, queryset, name, value):
        if self.request.GET.get('filter') == self.OWNERS_OF_FAVORITE_PROJECTS_NAME:
            return queryset.filter(
                owned_projects__in=(self.request.user.favorites.all())
            ).distinct()
        return queryset

    def filter_owners_of_participating_projects(self, queryset, name, value):
        if self.request.GET.get('filter') == self.OWNERS_OF_PARTICIPATING_PROJECTS:
            return queryset.filter(
                owned_projects__in=(self.request.user.participated_projects.all())
            ).distinct()
        return queryset

    def filter_interested_in_my_projects(self, queryset, name, value):
        if self.request.GET.get('filter') == self.INTERSETED_IN_MY_PROJECTS:
            return queryset.filter(
                favorites__in=(self.request.user.owned_projects.all())
            ).distinct()
        return queryset

    def filter_participants_of_my_projects(self, queryset, name, value):
        if self.request.GET.get('filter') == self.PARTICIPANTS_OF_MY_PROJECTS:
            return queryset.filter(
                participated_projects__in=(self.request.user.owned_projects.all())
            ).distinct()
        return queryset
