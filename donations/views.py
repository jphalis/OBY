from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from donations.forms import DonationForm
from ecomm.forms import StripeCreditCardForm
from .models import Donation


@login_required
@cache_page(60 * 5)
def info(request):
    total_amount = Donation.objects.aggregate(Sum('amount')).values()[0]
    donations = Donation.objects.select_related('user')

    context = {
        'donations': donations,
        'total_amount': total_amount
    }
    return render(request, 'donations/info.html', context)


@login_required
@cache_page(60 * 3)
def make(request):
    credit_card_form = StripeCreditCardForm(request.POST or None,
                                            user=request.user)
    donation_form = DonationForm(request.POST or None, user=request.user)

    if request.method == 'POST' and credit_card_form.is_valid() \
            and donation_form.is_valid():

        # create charge at Stripe
        charge = credit_card_form.charge_customer(
            amount=donation_form.cleaned_data.get('amount'),
            description='Donation from {} to OBY'.format(request.user.email)
        )

        if charge:
            # persist charge ID returned from Stripe
            donation_form.charge_id = charge.id
            donation_form.save()

            messages.success(request, "Thank you for your donation!")
            return HttpResponseRedirect(reverse('donations:info'))

        else:
            messages.error(request,
                           "We're sorry, but your credit card "
                           "could not be charged at this time. "
                           "We regret that this has occured. "
                           "Please try again later.")

    context = {
        'credit_card_form': credit_card_form,
        'donation_form': donation_form
    }
    return render(request, 'donations/make.html', context)
