from django.contrib import admin

from django.contrib.auth.models import Group

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth import get_user_model

from .forms import UserChangeForm, UserCreationForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email', 'name', 'surname']
    list_filter = ['is_staff']
    # fieldsets = [
    #   (None, {"fields": ["email", "password"]}),
    #    ("Personal info", {"fields": ["date_of_birth"]}),
    #   ("Permissions", {"fields": ["is_admin"]}),
    # ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # add_fieldsets = [
    #    (
    #        None,
    #        {
    #            "classes": ["wide"],
    #            "fields": ["email", "date_of_birth", "password1", "password2"],
    #        },
    #    ),
    # ]
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
