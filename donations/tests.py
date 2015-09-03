from datetime import datetime
import mock
from mock import Mock, MagicMock

from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from accounts.models import MyUser
from .forms import DonationForm
from .models import Donation


def make_user(username='testuser', email='test@user.com', password='testuser'):
    return MyUser.objects.create_user(username=username, email=email,
        password=password)


class DonationFormUnitTest(TestCase):

    def test_charge_id_persisted(self):

        # create user
        user = make_user()

        form = DonationForm(data={'amount': 10}, charge_id='abc123',
            user=user)

        self.assertTrue(form.is_valid(), "DonationForm should be valid")

        donation = form.save()
        self.assertEqual(donation.charge_id, 'abc123', "Donation charge_id "
            "should be: abc123. Instead was: {}".format(donation.charge_id))

    def test_amount_greater_than_zero(self):
        # create user
        user = make_user()

        form = DonationForm(data={'amount': 0}, charge_id='abc123', user=user)
        self.assertFalse(form.is_valid(), "Form should not be valid with 0 "
            "for amount.")


class DonationViewsFunctionalTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.make_donation_url = reverse('donations:make')

    @mock.patch('donations.views.StripeCreditCardForm.create_card')
    @mock.patch('donations.views.StripeCreditCardForm.charge_customer')
    def test_valid_post_data_creates_donation(self, mock_charge_customer, mock_create_card):

        # create user
        user = make_user()

        # login
        self.client.login(username='testuser', password='testuser')

        mock_create_card.return_value = True
        mock_charge_customer.return_value = MagicMock(id='abc123')

        # post data
        data = {'card_number': '4242424242424242',
            'expire_month': 12,
            'expire_year': datetime.now().year + 1,
            'cvc': 123, 'amount': 10, 'message': 'Test Donation'}

        # make post request
        response = self.client.post(self.make_donation_url, data,
            follow=True)

        # donations:make should redirect on a successful post.
        # assert 200 status code returned
        self.assertEqual(response.status_code, 200, "A successful "
            "post to donations:make should redirect to the 'complete' "
            "view.")

        # assert donations:make redirected to the correct place
        complete_url = reverse('donations:complete')
        request_path = response.request['PATH_INFO']
        self.assertEqual(request_path, complete_url, "donations:make did "
            "not redirect to 'donations:complete' instead was: {}".format(
                request_path))

        # assert Donation information correct
        try:
            donation = Donation.objects.filter(user=user)[:1][0]
        except Donation.DoesNotExist:
            donation = None

        self.assertIsNotNone(donation, "Donation was not created.")

        donation_amount = int(donation.amount)
        expected_amount = data['amount']
        self.assertEqual(donation_amount, expected_amount, "Donation amount "
            "is not correct. Expected: {}. Was: ".format(expected_amount,
                donation_amount))

        expected_charge_id = 'abc123'
        self.assertEqual(donation.charge_id, expected_charge_id,
            "Donation charge id is not correct. Expected: {} instead was "
            "{}".format(expected_charge_id, donation.charge_id))

    @mock.patch('donations.views.StripeCreditCardForm.create_card')
    @mock.patch('donations.views.StripeCreditCardForm.charge_customer')
    def test_invalid_post_data_fails(self, mock_charge_customer, mock_create_card):

        # create user
        user = make_user()

        # login
        self.client.login(username='testuser', password='testuser')

        mock_create_card.return_value = True
        mock_charge_customer.return_value = MagicMock(id='abc123')

        # post data
        data = {'card_number': '4242424242424242',
            'expire_month': 12,
            'expire_year': datetime.now().year,
            'cvc': 123, 'amount': 0, 'message': 'Test Donation'}

        # make post request
        response = self.client.post(self.make_donation_url, data,
            follow=True)

        # donations:make should redirect on a successful post.
        # assert 200 status code returned
        self.assertEqual(response.status_code, 200, "donation:make view "
            "should return a 200 even on a failed post.")

        # assert failed post does not create a donation object
        self.assertEqual(Donation.objects.filter(amount=0, user=user).count(),
            0, "Donation should not be created on a failed POST.")

    @mock.patch('donations.views.StripeCreditCardForm.create_card')
    @mock.patch('donations.views.StripeCreditCardForm.charge_customer')
    def test_charge_failure(self, mock_charge_customer, mock_create_card):

        # create user
        user = make_user()

        # login
        self.client.login(username='testuser', password='testuser')

        mock_create_card.return_value = True

        # simulate charge failure
        mock_charge_customer.return_value = None

        # post data
        data = {'card_number': '4242424242424242',
            'expire_month': 12,
            'expire_year': datetime.now().year,
            'cvc': 123, 'amount': 10, 'message': 'Test Donation'}

        # make post request
        response = self.client.post(self.make_donation_url, data,
            follow=True)

        # if charge fails, donations:make should be rendered again
        self.assertEqual(response.status_code, 200, "donation:make view "
            "should return a 200 even if the charge can't be created.")

        self.assertEqual(response.request['PATH_INFO'],
            reverse('donations:make'), "Path rendered does not match "
            "donations:make")

        # assert failed charge does not create a donation object
        self.assertEqual(Donation.objects.filter(amount=0, user=user).count(),
            0, "Donation should not be created on a failed POST.")
