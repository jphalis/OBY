from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _

from .models import MyUser
from .forms import UserChangeForm, UserCreationForm


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'is_superuser', 'is_admin', 'is_verified',
                    'date_joined')
    list_filter = ('is_active', 'is_admin', 'is_verified')
    readonly_fields = ['date_joined', 'last_login', 'modified']
    fieldsets = (
        (None,
            {'fields': ('username', 'email', 'password',)}),
        ('Additional information',
            {'fields': ('full_name', 'edu_email', 'gender', 'bio', 'website',
                        'profile_picture',)}),
        # ('Points',
        #     {'fields': ('available_points', 'total_points',
        #                 'creations_allowed',)}),
        ('Permissions',
            {'fields': ('is_active', 'is_admin',
                        'is_verified', 'user_permissions')}),
        (_('Dates'),
            {'fields': ('date_joined', 'last_login', 'modified',)}),
    )

    add_fieldsets = (
        (None,
            {'classes': ('wide',),
             'fields': ('username', 'email', 'password1', 'password2',)}),
    )
    search_fields = ('email', 'username', 'full_name',)
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)

admin.site.register(MyUser, MyUserAdmin)
admin.site.unregister(Group)
