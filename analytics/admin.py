from django.contrib import admin

from .models import PageView

# Register your models here.


class PageViewAdmin(admin.ModelAdmin):
    list_display = ['__unicode__']
    readonly_fields = ['created']
    search_fields = ['user__username']

    class Meta:
        model = PageView

admin.site.register(PageView, PageViewAdmin)
