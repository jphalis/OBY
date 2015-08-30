from django import forms

from decimal import Decimal

from .models import Donation

# Create forms here.


# Make a model form
class DonationForm(forms.ModelForm):
    amount = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"placeholder": "$0.00"}))
    name = forms.CharField(
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": "Name"})
    )
    email = forms.EmailField(max_length=80,
                             widget=forms.widgets.EmailInput(
                                attrs={'placeholder': 'Email'}))
    message = forms.CharField(
        max_length=4000, required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Leave a message for us",
                   "style": "height: 6em;"})
    )

    class Meta:
        model = Donation
        fields = ('amount', 'name', 'email', 'message')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        two_places = Decimal(10) ** -2
        total_dec = Decimal(amount).quantize(two_places)
        amount = total_dec
        return amount

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        return email
