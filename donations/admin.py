from django.contrib import admin

from .models import Donation

# Register your models here.


class DonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'donation_id', 'modified']
    search_fields = ['user__username', 'donation_id']
    readonly_fields = ['created', 'modified']

    class Meta:
        model = Donation
        fields = '__all__'

admin.site.register(Donation, DonationAdmin)
