from django.contrib import admin

from django.contrib.auth.models import Group

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth import get_user_model

from .forms import AdminUserChangeForm, UserCreationForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'name', 'surname']
    list_filter = ['is_staff']
    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        (
            'Personal info',
            {"fields": ['avatar', 'name', 'surname', 'about', 'phone', 'github_url']},
        ),
        ('Permissions', {"fields": ['is_active', 'is_staff']}),
    ]
    add_fieldsets = [
        (
            None,
            {
                'fields': ['name', 'surname', 'email', 'password'],
            },
        ),
    ]
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
