from django.contrib import admin

from .models import Donation


class DonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'charge_id']
    search_fields = ['user__username', 'charge_id']
    readonly_fields = ['created', 'modified']

admin.site.register(Donation, DonationAdmin)
