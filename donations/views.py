import stripe

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render

from .forms import DonationForm
from .models import Donation

# Create your views here.


@login_required
def make_donation(request):
    donation_form = DonationForm(request.POST or None)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    pub_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        token = request.POST['stripeToken']

        if donation_form.is_valid():
            amount = donation_form.cleaned_data['amount']
            email = donation_form.cleaned_data['email']

            obj = donation_form.save(commit=False)
            obj.user = request.user
            obj.amount = amount
            obj.email = email
            obj.save()

            context = {'amount': amount}

            try:
                charge = stripe.Charge.create(
                    amount=1000,  # amount in cents, again
                    currency="usd",
                    source=token,
                    description="OBY donation"
                )
                # return HttpResponseRedirect(reverse("donation_complete"))
                # Place message on this template ^
                messages.success(request,
                                 "Thank you for your contribution! "
                                 "It's because of people like you that "
                                 "we are able to make a difference together!")
            except stripe.error.CardError, e:
                # The card has been declined
                messages.error(request,
                               "We're sorry, but your card has been declined. "
                               "Please try again!")
                pass
    context = {
        'donation_form': donation_form,
        'pub_key': pub_key
    }
    return render(request, 'donations/make_donation.html', context)


@login_required
def donation_complete(request):
    context = {}
    return render(request, 'donations/donation_complete.html', context)


@login_required
def donation_history(request):
    history = Donation.objects.filter(user=request.user, status='Finished')
    context = {
        'history': history
    }
    return render(request, "donations/donation_history.html", context)
