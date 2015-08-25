# from decimal import Decimal
# from django.conf import settings
# from django.contrib.auth.models import User
# from django.db import models

# from profiles.models import UserAddress
# from carts.models import Cart

# # Create your models here.

# STATUS_CHOICES = (
#     ("Started", "Started"),
#     ("Abandoned", "Abandoned"),
#     ("Finished", "Finished"),
# )

# try:
#     tax_rate = settings.DEFAULT_TAX_RATE
# except Exception, e:
#     raise NotImplementedError(str(e))

# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
#     order_id = models.CharField(max_length=120, default="ABC", unique=True)
#     cart = models.ForeignKey(Cart)
#     number_of_lessons = models.DecimalField(default=1, max_digits=100, decimal_places=1)
#     status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
#     shipping_address = models.ForeignKey(UserAddress, related_name="shipping_address", default=1)
#     billing_address = models.ForeignKey(UserAddress, related_name="billing_address", default=1)
#     sub_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
#     tax_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2)
#     final_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
#     updated = models.DateTimeField(auto_now_add=False, auto_now=True)

#     def __unicode__(self):
#         return self.order_id

#     class Meta:
#         ordering = ['-updated', '-timestamp']

#     def get_lesson_final_amount(self):
#         instance = Cart.objects.get(id=self.id)
#         final_number_of_lessons = Decimal(self.number_of_lessons)
#         instance.number_of_lessons = final_number_of_lessons
#         instance.save()
#         return instance.number_of_lessons

#     def get_sub_total_amount(self):
#         instance = Order.objects.get(id=self.id)
#         two_places = Decimal(10) ** -2
#         sub_total_dec = Decimal(self.sub_total)
#         instance.sub_total = sub_total_dec
#         instance.save()
#         return instance.sub_total

#     def get_tax_total_amount(self):
#         instance = Order.objects.get(id=self.id)
#         two_places = Decimal(10) ** -2
#         tax_rate_dec = Decimal("%s" %(tax_rate))
#         sub_total_dec = Decimal(self.sub_total)
#         tax_total_dec = Decimal(tax_rate_dec * sub_total_dec).quantize(two_places)
#         instance.tax_total = tax_total_dec
#         instance.save()
#         return instance.tax_total

#     def get_final_amount(self):
#         instance = Order.objects.get(id=self.id)
#         two_places = Decimal(10) ** -2
#         tax_rate_dec = Decimal("%s" %(tax_rate))
#         sub_total_dec = Decimal(self.sub_total)
#         tax_total_dec = Decimal(tax_rate_dec * sub_total_dec).quantize(two_places)
#         instance.tax_total = tax_total_dec
#         instance.final_total = sub_total_dec + tax_total_dec
#         instance.save()
#         return instance.final_total
