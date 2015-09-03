from datetime import date

from django.test import TestCase

from accounts.models import MyUser
from .forms import StripeCreditCardForm


class StripeCreditCardFormUnitTest(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(
            username='test',
            password='pbkdf2_sha256$12000$64NIBRztT1eL$ip9P9F2vYdCvIXMQlDNt/Hm+8grJp6nbvj4GZjRVHxc=',
            email='test@user.com', is_active=True, full_name='Test User')

    def test_get_expire_months(self):
        expected_expire_month_choices = [
            ('01', '01',),
            ('02', '02',),
            ('03', '03',),
            ('04', '04',),
            ('05', '05',),
            ('06', '06',),
            ('07', '07',),
            ('08', '08',),
            ('09', '09',),
            ('10', '10',),
            ('11', '11',),
            ('12', '12',)
        ]

        form = StripeCreditCardForm(user=self.user)
        expire_month_choices = form.fields['expire_month'].choices
        self.assertEqual(expire_month_choices,
            expected_expire_month_choices, 'Expire month choices were not '
            'equal. Expected: {}. Instead was: {}'.format(
                expected_expire_month_choices, expire_month_choices))

    def test_get_expire_years(self):
        current_year = date.today().year
        expected_expire_year_choices = [
            (str(current_year), str(current_year),),
            (str(current_year + 1), str(current_year + 1),),
            (str(current_year + 2), str(current_year + 2),),
            (str(current_year + 3), str(current_year + 3),),
            (str(current_year + 4), str(current_year + 4),),
            (str(current_year + 5), str(current_year + 5),),
            (str(current_year + 6), str(current_year + 6),),
            (str(current_year + 7), str(current_year + 7),),
            (str(current_year + 8), str(current_year + 8),),
            (str(current_year + 9), str(current_year + 9),),
            (str(current_year + 10), str(current_year + 10),),
            (str(current_year + 11), str(current_year + 11),)
        ]

        form = StripeCreditCardForm(user=self.user)
        expire_year_choices = form.fields['expire_year'].choices
        self.assertEqual(expire_year_choices,
            expected_expire_year_choices, 'Expire year choices were not '
            'equal. Expected: {}. Instead was: {}'.format(
                expected_expire_year_choices, expire_year_choices))

    def test_strip_non_numeric_characters(self):
        value = '1111-1111-1111-1111'
        expected_result = value.replace('-', '')
        form = StripeCreditCardForm(user=self.user)
        actual_result = form.strip_non_numbers(value)
        self.assertEqual(expected_result, actual_result, 'Expected result: '
            '{} did not match actual result: {}'.format(expected_result,
                                                        actual_result))

    def test_luhn_checksum(self):
        card_data = {
            'expire_month': '12',
            'expire_year': '{}'.format(date.today().year + 1),
            'cvc': '111'
        }

        # bad credit card number
        card_data['card_number'] = '0123-4567-9089-0000'
        form1 = StripeCreditCardForm(user=self.user, data=card_data)

        # call .is_valid() to populate cleaned data
        form1.is_valid()
        self.assertFalse(form1.card_luhn_checksum_valid(),
            'Card number should not be valid.')

        # good credit card number
        card_data['card_number'] = '4242-4242-4242-4242'
        form2 = StripeCreditCardForm(user=self.user, data=card_data)

        form2.is_valid()
        self.assertTrue(form2.card_luhn_checksum_valid(),
            'Card number should be valid.')
