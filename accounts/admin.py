from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _

from photos.models import Photo
from .models import MyUser
from .forms import UserChangeForm, UserCreationForm


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'is_superuser', 'is_admin', 'is_verified',
                    'date_joined', 'times_flagged')
    list_filter = ('is_active', 'is_admin', 'is_verified')
    readonly_fields = ['date_joined', 'last_login', 'modified',
                       'times_flagged']
    fieldsets = (
        (None,
            {'fields': ('username', 'email', 'password',)}),
        ('Basic information',
            {'fields': ('full_name', 'edu_email', 'gender', 'bio', 'website',
                        'profile_picture',)}),
        ('Points',
            {'fields': ('available_points', 'total_points',)}),
        ('Permissions',
            {'fields': ('is_active', 'is_admin',
                        'is_verified', 'user_permissions')}),
        (_('Dates'),
            {'fields': ('date_joined', 'last_login', 'modified',)}),
        (_('Flags'),
            {'fields': ('times_flagged',)}),
    )

    add_fieldsets = (
        (None,
            {'classes': ('wide',),
             'fields': ('username', 'email', 'password1', 'password2',)}),
    )
    search_fields = ('email', 'username', 'full_name',)
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)
    actions = ('activate', 'disable', 'verified',)

    def activate(self, request, queryset):
        queryset.update(is_active=True)
        Photo.objects.filter(creator=queryset).update(is_active=True)
    activate.short_description = _("Activate selected users")

    def disable(self, request, queryset):
        queryset.update(is_active=False)
        Photo.objects.filter(creator=queryset).update(is_active=False)
    disable.short_description = _("Disable selected users")

    def verified(self, request, queryset):
        queryset.update(is_verified=True)
    verified.short_description = _("Verify selected users")

admin.site.register(MyUser, MyUserAdmin)
admin.site.unregister(Group)
