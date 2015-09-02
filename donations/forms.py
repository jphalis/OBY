from django import forms

from .models import Donation


class DonationForm(forms.ModelForm):
    """
    Used to gather message from user. Donation transaction is handled
    through StripeEcommerceForm.
    """

    class Meta:
        fields = ('amount', 'message',)
        model = Donation

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        if 'charge_id' in kwargs:
            self.charge_id = kwargs.pop('charge_id')

        super(DonationForm, self).__init__(*args, **kwargs)

        self.fields['amount'].initial = None

    def clean_donation(self):
        donation = self.cleaned_data.get('donation')

        if donation == 0:
            raise forms.ValidationError('Please enter a value greater than 0.')

        return donation

    def save(self, commit=True):
        instance = super(DonationForm, self).save(commit=False)

        if commit:
            instance.user = self.user
            instance.charge_id = self.charge_id
            instance.save()

        return instance
