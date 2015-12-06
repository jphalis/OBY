# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from django.shortcuts import (get_object_or_404, Http404,
#                               HttpResponseRedirect, redirect, render)
# from django.utils import timezone

# from analytics.signals import page_view

# from .forms import ComposeForm, ReplyForm
# from .models import DirectMessage

# # Create your views here.


# # Long-term, this will be like the comments - have all in one window
# @login_required
# def reply(request, id):
#     if request.method == "POST":
#         parent_id = id
#         parent = get_object_or_404(DirectMessage, id=parent_id)
#         form = ReplyForm(request.POST, request.FILES)
#         if form.is_valid():
#             send_message = form.save(commit=False)
#             send_message.sender = request.user
#             send_message.recipient = parent.sender
#             send_message.sent = timezone.now()
#             send_message.parent = parent
#             send_message.save()
#             messages.success(request, "Your reply has been sent!")
#             parent.replied = True
#             parent.save()
#             return HttpResponseRedirect(reverse('direct_messages'))
#     else:
#         form = ReplyForm()

#     context = {
#         "form": form
#     }
#     return render(request, "directmessages/reply.html", context)


# @login_required
# def view_direct_message(request, id):
#     user = request.user
#     message = get_object_or_404(DirectMessage, id=id)

#     if message.sender == user or message.recipient == user:
#         if not message.opened:
#             message.read_at = timezone.now()
#             message.opened = True
#             message.save()
#             return render(request,
#                           'directmessages/view_direct_message.html',
#                           {'message': message})
#     else:
#         raise Http404


# @login_required
# def direct_messages(request):
#     user = request.user
#     inbox_messages = DirectMessage.objects.filter(recipient=user)

#     if request.method == "POST":
#         form = ComposeForm(request.POST, request.FILES)
#         if form.is_valid():
#             send_message = form.save(commit=False)
#             send_message.sender = request.user
#             send_message.sent = timezone.now()
#             send_message.save()
#             messages.success(request, "Your message has been sent!")
#             return HttpResponseRedirect(reverse('direct_messages'))
#     else:
#         form = ComposeForm()

#     context = {
#         "form": form,
#         "inbox_messages": inbox_messages
#     }
#     return render(request, "directmessages/direct_messages.html", context)


# @login_required
# def sent(request):
#     user = request.user
#     sent_messages = DirectMessage.objects.filter(sender=user)

#     context = {
#         'sent_messages': sent_messages
#     }
#     return render(request, 'directmessages/sent.html', context)
