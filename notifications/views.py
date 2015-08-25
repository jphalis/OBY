from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import Http404, render
from django.views.decorators.http import require_http_methods

from .models import Notification

# Create your views here.


@login_required
def all(request):
    notifications = Notification.objects.all_for_user(request.user)[:50]
    for notification in notifications:
        if notification.recipient == request.user:
            notification.read = True
            notification.save()
        else:
            raise Http404

    context = {
        "notifications": notifications
    }
    return render(request, "notifications/notifications_all.html", context)


@login_required
@require_http_methods(['POST'])
def get_notifications_ajax(request):
    notifications = Notification.objects.all_unread(request.user)
    count = notifications.count()
    data = {
        "count": count
    }
    return JsonResponse(data)
