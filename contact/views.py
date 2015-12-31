from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect, render
from django.views.decorators.cache import cache_page

from .forms import BusinessContactForm

# Create your views here.


@cache_page(60 * 12)
def business_inquiry(request):
    form = BusinessContactForm(request.POST or None)

    if form.is_valid():
        form_name = form.cleaned_data['name']
        form_organization = form.cleaned_data['organization']
        form_email = form.cleaned_data['email']
        form_coupons = form.cleaned_data['coupons']
        form_expectations = form.cleaned_data['expectations']
        subject = 'Business Inquiry Form'
        from_email = 'partnerships@obystudio.com'
        to_email = ['partnerships@obystudio.com']
        contact_message = "Name: {} \nOrganization: {} \nEmail: {} \
        \nOffer coupons: {} \nExpectations: {}".format(
            form_name,
            form_organization,
            form_email,
            form_coupons,
            form_expectations,
        )
        send_mail(
            subject,
            contact_message,
            from_email,
            to_email,
            fail_silently=True
        )
        messages.success(request,
                         "Thank you for your message. \
                         We have received it, and will be in touch soon!")
        return HttpResponseRedirect(reverse("home"))
    return render(request, 'company/business_inquiry.html', {'form': form})
