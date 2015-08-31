from django.contrib import admin

from .models import Newsletter

# Register your models here.


class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', '__unicode__']
    list_filter = ['subscribed']
    readonly_fields = ['created', 'modified']
    search_fields = ['user__username']

    class Meta:
        model = Newsletter

admin.site.register(Newsletter, NewsletterAdmin)
