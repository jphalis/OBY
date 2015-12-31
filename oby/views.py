# from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import HttpResponseRedirect, render
from django.views.decorators.cache import cache_page

# from accounts.models import Follower
# from photos.models import Category, Photo

# Create views here.


@cache_page(60 * 7)
def home(request):
    # if request.user.is_authenticated():
    #     categories = Category.objects.most_posts()
    #     photos = Photo.objects.most_liked_offset()[:30]

    #     context = {
    #         'categories': categories,
    #         'photos': photos
    #     }
    #     return render(request, 'accounts/home_logged_in.html', context)
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse(
            'profile_view', kwargs={"username": request.user.username}))
    return render(request, 'visitor/home_visitor.html', {})


@login_required
@cache_page(60 * 2)
def timeline(request):
    # user = request.user

    # try:
    #     follow = Follower.objects.get(user=user)
    # except Follower.DoesNotExist:
    #     follow = None

    # photos_self = Photo.objects.own(user)

    # if follow:
    #     photos_following = Photo.objects.following(user)
    #     photos = (photos_following | photos_self).distinct()[:250]
    # else:
    #     # Add suggested users
    #     photos_suggested = Photo.objects.all() \
    #         .select_related("creator", "category") \
    #         .prefetch_related('likers') \
    #         .exclude(creator=user)[:50]
    #     photos = chain(photos_self, photos_suggested)

    # context = {
    #     'follow': follow,
    #     'photos': photos
    # }
    # return render(request, 'accounts/timeline.html', context)
    raise Http404


@cache_page(60 * 60 * 24 * 300)
def about(request):
    return render(request, 'company/about.html', {})


@cache_page(60 * 60 * 24 * 300)
def privacy_policy(request):
    return render(request, 'company/privacy_policy.html', {})


@cache_page(60 * 60 * 24 * 300)
def terms_of_use(request):
    return render(request, 'company/terms_of_use.html', {})


# @login_required(login_url='/staff/login/')
# def staff_home(request):
#     context = {}
#     return render(request, "home.html", context)
