from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMessage, send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.template import Context
from django.template.loader import get_template
from django.utils.html import escape
from django.views.decorators.cache import cache_page

from accounts.models import Advertiser, MyUser
from accounts.forms import RegisterForm
from .forms import BusinessContactForm

# Create your views here.


@cache_page(60 * 12)
def business_inquiry(request):
    form = BusinessContactForm(request.POST or None)

    if form.is_valid():
        form_name = escape(form.cleaned_data['name'])
        form_company = escape(form.cleaned_data['company'])
        form_email = escape(form.cleaned_data['email'])
        form_coupons = escape(form.cleaned_data['coupons'])
        form_message = escape(form.cleaned_data['message'])

        subject = 'Business Inquiry Form'
        from_email = 'partnerships@obystudio.com'
        to_email = ['halis@obystudio.com']
        contact_message = "Name: {} | Organization: {} | Email: {} \
        | Offer coupons: {} | Message: {}".format(
            form_name,
            form_company,
            form_email,
            form_coupons,
            form_message,
        )
        send_mail(
            subject,
            contact_message,
            from_email,
            to_email,
            fail_silently=True
        )
        if form_coupons == "Yes" or "Maybe":
            context = {'domain': request.get_host()}
            message = get_template(
                'advertisers/business_inquiry_email.html').render(
                Context(context))
            email = EmailMessage(
                'OBY Partnership Inquiry',
                message,
                from_email,
                ['{}'.format(form_email)]
            )
            email.content_subtype = 'html'
            email.send()
        messages.success(request,
                         "Thank you for your message. \
                         We have received it, and will be in touch soon!")
        return HttpResponseRedirect(reverse("home"))
    return render(request, 'advertisers/business_inquiry.html', {'form': form})


def business_signup(request):
    if request.user.is_authenticated():
        return redirect("home")
    else:
        form = RegisterForm(request.POST or None)
        next_url = request.POST.get('next')

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            new_user = MyUser()
            new_user.username = username
            new_user.email = email
            new_user.set_password(password)
            new_user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                new_advertiser, created = Advertiser.objects.get_or_create(
                    user=user)
                new_advertiser.save()
                login(request, user)

                if next_url is not None:
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect(reverse("home"))
        context = {
            "form": form,
            "action_url": reverse("contact:business_signup"),
        }
        return render(request, 'advertisers/business_signup.html', context)
