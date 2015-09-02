from decimal import Decimal

from django.test import TestCase

from accounts.models import MyUser
from .forms import DonationForm


class DonationFormUnitTest(TestCase):

    def setUp(self):
        my_user, created = MyUser.objects.get_or_create(
            username='test',
            password='pbkdf2_sha256$12000$64NIBRztT1eL$ip9P9F2vYdCvIXMQlDNt/Hm+8grJp6nbvj4GZjRVHxc=',
            email='test@user.com', is_active=True, full_name='Test User')

        self.user = my_user

    def test_charge_id_persisted(self):
        form = DonationForm(data={'amount': 10}, charge_id='abc123',
            user=self.user)

        self.assertTrue(form.is_valid(), "DonationForm should be valid")

        donation = form.save()
        self.assertEqual(donation.charge_id, 'abc123', "Donation charge_id "
            "should be: abc123. Instead was: {}".format(donation.charge_id))
