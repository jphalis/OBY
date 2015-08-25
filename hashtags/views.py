from django.db.models import Q
from django.shortcuts import render

from photos.models import Photo

# Create your views here.


def hashtagged_item_list(request, tag):
    photos = Photo.objects.filter(Q(description__icontains=tag))[:200]

    context = {
        'photos': photos,
        'tag': tag
    }
    return render(request, 'hashtags/hashtagged_item_list.html', context)
