import django_filters
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFilter(django_filters.FilterSet):
    owners_of_favorite_projects = django_filters.CharFilter(
        method='filter_owners_of_favorite_projects',
        widget=forms.CheckboxInput(attrs={'name': 'owners-of-favorite-projects'}),
    )

    owners_of_participating_projects = django_filters.CharFilter(
        method='filter_owners_of_participating_projects',
        widget=forms.CheckboxInput(attrs={'name': 'owners-of-participating-projects'}),
    )

    interested_in_my_projects = django_filters.CharFilter(
        method='filter_interested_in_my_projects',
        widget=forms.CheckboxInput(attrs={'name': 'interested-in-my-projects'}),
    )

    participants_of_my_projects = django_filters.CharFilter(
        method='filter_participants_of_my_projects',
        widget=forms.CheckboxInput(attrs={'name': 'participants-of-my-projects'}),
    )

    class Meta:
        model = User
        fields = []

    def filter_owners_of_favorite_projects(self, queryset, name, value):
        if self.request.GET.get('filter') == 'owners-of-favorite-projects':
            return queryset.filter(
                owned_projects__in=(self.request.user.favorites.all())
            ).distinct()
        return queryset

    def filter_owners_of_participating_projects(self, queryset, name, value):
        if self.request.GET.get('filter') == 'owners-of-participating-projects':
            return queryset.filter(
                owned_projects__in=(self.request.user.participated_projects.all())
            ).distinct()
        return queryset

    def filter_interested_in_my_projects(self, queryset, name, value):
        if self.request.GET.get('filter') == 'interested-in-my-projects':
            return queryset.filter(
                favorites__in=(self.request.user.owned_projects.all())
            ).distinct()
        return queryset

    def filter_participants_of_my_projects(self, queryset, name, value):
        if self.request.GET.get('filter') == 'participants-of-my-projects':
            return queryset.filter(
                participated_projects__in=(self.request.user.owned_projects.all())
            ).distinct()
        return queryset
