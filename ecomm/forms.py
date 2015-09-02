import re

from django import forms
from django.conf import settings
from django.template.defaultfilters import mark_safe
from django.utils import timezone

import stripe


class StripeCreditCardForm(forms.Form):
    card_number = forms.CharField(label='* Card Number')
    expire_month = forms.ChoiceField(label='* Expriration')
    expire_year = forms.ChoiceField(label=mark_safe('&nbsp;'))
    cvc = forms.CharField(max_length=5, min_length=3, label='* CVC')

    def __init__(self, *args, **kwargs):
        # user is passed in since we create it with the account sign up
        self.user = kwargs.pop('user')

        super(StripeCreditCardForm, self).__init__(*args, **kwargs)
        self.token = None
        self.amount = None
        self.stripe = stripe

        # assume test mode
        api_key = settings.TEST_STRIPE_API_KEY
        if settings.STRIPE_MODE == 'live':
            settings.STRIPE_API_KEY
        self.stripe.api_key = api_key

        # set expire months/years
        expire_month = self.fields['expire_month']
        expire_month.choices = self.get_expire_months()

        expire_year = self.fields['expire_year']
        expire_year.choices = self.get_expire_years()

    def card_luhn_checksum_valid(self):
        # Checks to make sure that the card passes a luhn mod-10 checksum

        card_number = self.strip_non_numbers(
            self.cleaned_data.get('card_number', ''))
        sum = 0
        num_digits = len(card_number)
        oddeven = num_digits & 1
        for count in range(0, num_digits):
            digit = int(card_number[count])
            if not ((count & 1) ^ oddeven):
                digit = digit * 2
            if digit > 9:
                digit = digit - 9
            sum = sum + digit
        return (sum % 10) == 0

    def strip_non_numbers(self, card_number):
        # gets rid of all non-numeric characters
        non_numbers = re.compile('\D')
        return non_numbers.sub('', card_number)

    def get_expire_months(self):
        months = []
        for month in range(1, 13):
            if len(str(month)) == 1:
                numeric = '0{}'.format(month)
            else:
                numeric = str(month)
            months.append((numeric, numeric))
        return months

    def get_expire_years(self):
        current_year = timezone.now().year
        years = range(current_year, current_year + 12)
        return [(str(year), str(year)) for year in years]

    def get_or_create_customer(self):
        try:
            customer = self.stripe.Customer.retrieve(
                self.user.stripe_customer_id)
        except stripe.error.InvalidRequestError:
            customer = self.stripe.Customer.create(
                description='Customer for {}'.format(self.user.email)
            )

            # persist customer id on user model
            self.user.stripe_customer_id = customer.id
            self.user.save()

        self.customer = customer
        return customer

    def create_card(self, card_number, expire_month, expire_year, cvc):
        customer = self.get_or_create_customer()

        try:
            # Create the card for the customer
            self.card = customer.sources.create(source={
                'object': 'card',
                'number': card_number,
                'exp_month': expire_month,
                'exp_year': expire_year,
                'cvc': cvc,
                'name': self.user.get_full_name()
            })

        except stripe.error.CardError:
            raise forms.ValidationError("Sorry, we weren't able to "
                "validate your credit card details at this time. Please try "
                "again later.")

    def charge_customer(self, amount, description):
        # Amount must be a positive integer in cents.
        try:
            charge = self.stripe.Charge.create(
                amount=int(amount) * 100,
                currency='usd',
                customer=self.customer.id,
                description=description,
                source=self.card
            )
        except self.stripe.CardError:
            raise forms.ValidationError(
                "We're sorry, your card could not be charged at this time.")
        return charge

    def clean(self):
        cleaned_data = self.cleaned_data

        # validate card checksum
        if not self.card_luhn_checksum_valid():
            raise forms.ValidationError(
                'The credit card you entered was invalid.')

        today = timezone.now().today()
        this_year = today.year
        this_month = today.month
        expire_month = int(cleaned_data.get('expire_month'))
        expire_year = int(cleaned_data.get('expire_year'))

        if expire_year == this_year and expire_month < this_month:
            raise forms.ValidationError('Expiration month must be greater '
                'than or equal to {} for {}'.format(this_month, this_year))

        # Validate card number and create Stripe token
        card_number = cleaned_data.get('card_number')
        cvc = cleaned_data.get('cvc')

        if card_number and cvc:
            # we aren't storing any card ids, so create a new one.
            # When the Stripe "card" object is created, is also functions
            # as the stripe "token".
            self.create_card(card_number, expire_month, expire_year, cvc)

        return cleaned_data
