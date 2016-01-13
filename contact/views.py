from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect, render
from django.utils.html import escape
from django.views.decorators.cache import cache_page

from .forms import BusinessContactForm

# Create your views here.


@cache_page(60 * 12)
def business_inquiry(request):
    form = BusinessContactForm(request.POST or None)

    if form.is_valid():
        form_name = escape(form.cleaned_data['name'])
        form_organization = escape(form.cleaned_data['organization'])
        form_email = escape(form.cleaned_data['email'])
        form_coupons = escape(form.cleaned_data['coupons'])
        form_expectations = escape(form.cleaned_data['expectations'])

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


#         email = EmailMessage(
#             subject,
#             contact_message,
#             from_email,
#             to_email,
#             headers={'Reply-To': form_email}
#         )
#         email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
#             ['to1@example.com', 'to2@example.com'], ['bcc@example.com'],
#             reply_to=['another@example.com'], headers={'Message-ID': 'foo'})
#         email.send()
