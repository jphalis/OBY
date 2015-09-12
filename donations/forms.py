from django import forms

from .models import Donation


class DonationForm(forms.ModelForm):
    """
    Used to gather message from user. Donation transaction is handled
    through StripeEcommerceForm.
    """
    amount = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"min": "1", "max": '15000'}))
    message = forms.CharField(
        max_length=2000, required=False,
        widget=forms.Textarea(
            attrs={"style": "height: 8em;",
                   "placeholder": "Leave a message for us. "
                                  "Only we will see it."})
    )

    class Meta:
        fields = ('amount', 'message', 'is_anonymous',)
        model = Donation

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        if 'charge_id' in kwargs:
            self.charge_id = kwargs.pop('charge_id')

        super(DonationForm, self).__init__(*args, **kwargs)

        self.fields['amount'].initial = None

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        if not amount > 0:
            raise forms.ValidationError(
                'Please enter an amount greater than 0')
        return amount

    def save(self, commit=True):
        instance = super(DonationForm, self).save(commit=False)

        if commit:
            instance.user = self.user
            instance.charge_id = self.charge_id
            instance.save()
        return instance
