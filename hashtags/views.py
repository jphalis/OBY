from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from photos.models import Photo

# Create your views here.


@cache_page(60 * 3)
def hashtagged_item_list(request, tag):
    photos = Photo.objects.filter(
        Q(description__icontains=tag) |
        Q(comment__hashtag_enabled_text__icontains=tag)
    )[:200]

    context = {
        'photos': photos,
        'tag': tag
    }
    return render(request, 'hashtags/hashtagged_item_list.html', context)
