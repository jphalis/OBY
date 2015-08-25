from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from itertools import chain

from accounts.models import Follower
from photos.models import Category, Photo

# Create views here.


@cache_page(60)
def home(request):
    if request.user.is_authenticated():
        categories = Category.objects.most_posts()
        photos = Photo.objects.most_liked_offset()[:30]

        context = {
            'categories': categories,
            'photos': photos
        }
        return render(request, 'accounts/home_logged_in.html', context)
    return render(request, 'visitor/home_visitor.html', {})


@login_required
@cache_page(60)
def timeline(request):
    user = request.user

    try:
        follow = Follower.objects.get(user=user)
    except Follower.DoesNotExist:
        follow = None

    photos_self = Photo.objects.own(user)

    if follow:
        photos_following = Photo.objects.following(user)
        photos = (photos_following | photos_self).distinct()[:250]
    else:
        # Add suggested users
        photos_suggested = Photo.objects.all().exclude(creator=user)[:50]
        photos = chain(photos_self, photos_suggested)

    context = {
        'follow': follow,
        'photos': photos
    }
    return render(request, 'accounts/timeline.html', context)


@cache_page(60 * 10)
def about(request):
    return render(request, 'company/about.html', {})


@cache_page(60 * 10)
def privacy_policy(request):
    return render(request, 'company/privacy_policy.html', {})


@cache_page(60 * 10)
def terms_of_use(request):
    return render(request, 'company/terms_of_use.html', {})


# @login_required(login_url='/staff/login/')
# def staff_home(request):
#     context = {}
#     return render(request, "home.html", context)
