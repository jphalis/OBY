from django.contrib import admin

from .models import Comment

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'path', 'text']
    search_fields = ['user__username']
    readonly_fields = ['created', 'modified']

    class Meta:
        model = Comment
        fields = '__all__'  # List all fields

admin.site.register(Comment, CommentAdmin)
