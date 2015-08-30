from django.contrib import admin

from .models import Donation

# Register your models here.


class DonationAdmin(admin.ModelAdmin):
    list_display = ['user', 'donation_id', 'updated']
    search_fields = ['user__username', 'donation_id']

    class Meta:
        model = Donation
        fields = '__all__'

admin.site.register(Donation, DonationAdmin)
