from django.contrib import admin

from .models import Notification

# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    # use if you want to limit which category is shown
    # form = PhotoUploadForm

    list_display = ['recipient', 'sender_object', 'created']
    fields = ['sender_object', 'recipient', 'created', 'modified']
    readonly_fields = ['created', 'modified']
    ordering = ['-created']

    class Meta:
        model = Notification


admin.site.register(Notification, NotificationAdmin)
