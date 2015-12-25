from django.contrib import admin

from .models import Notification

# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    # use if you want to limit which category is shown
    # form = PhotoUploadForm

    list_display = ['id', 'recipient', '__unicode__', 'read']
    list_filter = ['read']
    readonly_fields = ['created', 'modified']

    class Meta:
        model = Notification


admin.site.register(Notification, NotificationAdmin)
