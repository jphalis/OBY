# from django.contrib import admin

# from .models import Product  # Add product Category eventually

# # Register your models here.


# class ProductAdmin(admin.ModelAdmin):
#     date_hierarchy = 'list_date_start'
#     search_fields = ['id', 'buyers__username',
#                      'owner__username', 'description']
#     list_display = ['id', '__unicode__', 'cost', 'discount_cost', 'listed']
#     list_filter = ['listed']
#     readonly_fields = ['buyers', 'timestamp']
#     prepopulated_fields = {'slug': ["title"], }

#     class Meta:
#         model = Product

# admin.site.register(Product, ProductAdmin)
