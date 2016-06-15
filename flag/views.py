from django.shortcuts import get_object_or_404

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from photos.models import Photo
from .models import Flag


@login_required
@require_http_methods(['POST'])
def flag_create_ajax(request):
    photo_pk = request.POST.get('photo_pk')
    photo = get_object_or_404(Photo, pk=photo_pk)
    photo_creator = photo.creator

    flagged, created = Flag.objects.get_or_create(photo=photo,
                                                  creator=request.user)
    flagged.flag_count = F('flag_count') + 1
    flagged.save()

    photo_creator.times_flagged = F('times_flagged') + 1
    photo_creator.save()

    send_mail('FLAGGED ITEM',
              'There is a new flagged item with the id: {}'.format(flagged.id),
              settings.EMAIL_FROM, ['team@obystudio.com'], fail_silently=True)

    data = {
        "photo_flagged": True,
    }
    return JsonResponse(data)
