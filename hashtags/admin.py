from django.contrib import admin

from .models import Hashtag

# Register your models here.


class HashtagAdmin(admin.ModelAdmin):
    list_display = ('tag',)

admin.site.register(Hashtag, HashtagAdmin)
