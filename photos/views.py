import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.utils.crypto import get_random_string
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import DeleteView

from notifications.signals import notify

from .forms import PhotoUploadForm
from .models import Category, Photo

# Create your views here.


@login_required
@require_http_methods(['POST'])
def like_ajax(request):
    user = request.user
    photo_pk = request.POST.get('photo_pk')
    photo = get_object_or_404(Photo, pk=photo_pk)

    if user in photo.likers.all():
        photo.likers.remove(user)
        viewer_has_liked = False
    else:
        photo.likers.add(user)
        viewer_has_liked = True

        notify.send(
            user,
            action=photo,
            target=photo,
            recipient=photo.creator,
            verb='liked'
        )

    photo.save()
    like_count = photo.likers.count()

    data = {
        'viewer_has_liked': viewer_has_liked,
        'like_count': like_count
    }
    return JsonResponse(data)


@login_required
@cache_page(18)
def category_detail(request, cat_slug):
    obj = get_object_or_404(Category, slug=cat_slug)

    most_liked = Photo.objects.category_detail(obj)[:600]
    photos = list(most_liked)[:250]
    random.shuffle(photos)

    if request.user.is_authenticated():
        context = {
            'obj': obj,
            'photos': photos
        }
    else:
        next_url = obj.get_absolute_url()
        return HttpResponseRedirect('{}?next={}'.format(
            (reverse('login'), next_url)))
    return render(request, 'photos/category_detail.html', context)


class PhotoDelete(DeleteView):
    model = Photo
    success_url = reverse_lazy('home')
    template_name = 'photos/photo_delete.html'


@login_required
@cache_page(60 * 10)
def photo_upload(request):
    form = PhotoUploadForm(request.POST or None,
                           request.FILES or None,
                           request=request)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.slug = get_random_string(length=10)
            obj.save()
            messages.success(request,
                             "Thank you! You have successfully uploaded "
                             "your picture!")
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'photos/photo_upload.html', {'form': form})
