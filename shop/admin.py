from django.contrib import admin

from .models import Product

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'list_date_start'
    search_fields = ['id', 'buyers__username',
                     'owner__user__username', 'description']
    list_display = ['id', '__unicode__', 'cost', 'discount_cost', 'is_listed']
    list_filter = ['is_listed']
    readonly_fields = ['buyers']
    prepopulated_fields = {'slug': ["title"], }

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
