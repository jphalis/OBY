from django.contrib import admin
from django.core.urlresolvers import reverse

from flag.models import Flag


class FlagAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'link_to_photo', 'resolved', 'flag_count']
    list_filter = ('flag_count', 'resolved',)
    search_fields = ['id', 'creator']
    fields = ['id', 'creator', 'photo', 'comment', 'resolved', 'flag_count',
              'created', 'modified']
    readonly_fields = ['id', 'flag_count', 'created', 'modified']
    ordering = ['resolved']

    class Meta:
        model = Flag

    def link_to_photo(self, obj):
        link = reverse("admin:photos_photo_change", args=[obj.photo.id])
        return u'<a href="%s">%s</a>' % (link, obj.photo.slug)
    link_to_photo.allow_tags = True

admin.site.register(Flag, FlagAdmin)


# hide/oby/admin/photos/photo/75/change/
