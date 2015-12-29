from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import HttpResponseRedirect

from .models import Newsletter

# Create your views here.


@login_required
def toggle_newsletter(request):
    newsletter, created = Newsletter.objects.get_or_create(
        user=request.user)

    if newsletter.subscribed:
        newsletter.subscribed = False
        newsletter.save()
    else:
        newsletter.subscribed = True
        newsletter.save()
    return HttpResponseRedirect(reverse(
        'profile_view',
        kwargs={'username': request.user.get_username()}))
    # raise Http404
