from django.contrib import admin

from .models import Category, Photo

# Register your models here.


class PhotoAdmin(admin.ModelAdmin):
    # use if you want to limit which category is shown
    # form = PhotoUploadForm

    list_display = ['creator', 'category', 'slug', 'created',
                    'is_active', 'featured', 'like_count']
    search_fields = ['creator__username']
    fields = ['creator', 'photo', 'category', 'slug',
              'description', 'is_active', 'featured']
    ordering = ['-likers']

    class Meta:
        model = Photo

    # use if you want to limit which category is shown
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(PhotoAdmin, self).get_form(request, obj, **kwargs)
    #     form.request = request
    #     return form

admin.site.register(Photo, PhotoAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'border_color', 'is_active', 'featured']
    fields = ['title', 'slug', 'border_color', 'is_active', 'featured']
    prepopulated_fields = {'slug': ["title"], }

    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)
