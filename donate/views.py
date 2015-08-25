# import stripe

# from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from django.conf import settings
# from django.contrib import messages
# from django.shortcuts import render

# from profiles.forms import UserAddressForm
# from profiles.models import UserAddress

# from .models import Order

# # Create your views here.


# stripe.api_key = settings.STRIPE_SECRET_KEY


# def orders(request):
#     context = {}
#     return render(request, 'orders/user.html', context)


# @login_required
# def checkout(request):
#     pub_key = settings.STRIPE_PUBLISHABLE_KEY
#     customer_id = request.user.userstripe.stripe_id
#     if request.method == 'POST':
#         token = request.POST['stripeToken']

#         try:
#             customer = stripe.Customer.retrieve(customer_id)
#             customer.cards.create(card=token)
#             charge = stripe.Charge.create(
#                 amount=1000,  # amount in cents, again
#                 currency="usd",
#                 customer=customer,
#                 description ="{}".format(request.user.email)
#             )
#         except stripe.CardError, e:
#             # The card has been declined
#             pass

#     context = {'pub_key': pub_key}
#     template = 'checkout.html'
#     return render(request, template, context)


# @login_required
# def donation_history(request):
#     history = Order.objects.filter(user=request.user).filter(status='Finished')
#     context = {"queryset": history}
#     return render(request, "donate/history.html", context)
