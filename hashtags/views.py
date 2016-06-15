from django.shortcuts import render
from django.views.decorators.cache import cache_page

from photos.models import Photo

# Create your views here.


@cache_page(60 * 3)
def hashtagged_item_list(request, tag):
    photos = (Photo.objects.filter(description__icontains='#{}'.format(tag))
                           .select_related('creator', 'category')
                           .prefetch_related('likers'))[:150]
    context = {
        'photos': photos,
        'tag': tag
    }
    return render(request, 'hashtags/hashtagged_item_list.html', context)
