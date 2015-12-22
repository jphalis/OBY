from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import (get_object_or_404,
                              HttpResponseRedirect, render)
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods

from notifications.signals import notify
from photos.models import Category, Photo
from .forms import CommentForm
from .models import Comment

# Create your views here.


@login_required
@cache_page(60 * 4)
def comments_all(request, cat_slug, photo_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    photo = get_object_or_404(Photo, category=category, slug=photo_slug)
    comment_form = CommentForm()
    comments = photo.comment_set.active()
    for c in comments:
        c.get_children()

    context = {
        "comments": comments,
        "comment_form": comment_form,
        "photo": photo
    }
    return render(request, "comments/comments_all.html", context)


@login_required
@cache_page(60 * 4)
def comment_thread(request, id):
    comment = get_object_or_404(Comment, id=id)
    form = CommentForm()

    context = {
        "comment": comment,
        "form": form
    }
    return render(request, "comments/comment_thread.html", context)


@login_required
@require_http_methods(['POST'])
def comment_create_view(request):
    user = request.user
    parent_id = request.POST.get('parent_id')
    photo_id = request.POST.get("photo_id")
    origin_path = request.POST.get("origin_path")
    parent_comment = None
    form = CommentForm(request.POST)

    photo = (Photo.objects.select_related('creator', 'category')
                          .get(id=photo_id))

    photo_creator = photo.creator

    if parent_id is not None:
        try:
            parent_comment = (Comment.objects.select_related('user', 'photo')
                                     .get(id=parent_id))
        except:
            parent_comment = None
        if parent_comment is not None and parent_comment.photo is not None:
            photo = parent_comment.photo

    if form.is_valid():
        comment_text = form.cleaned_data['comment']
        if parent_comment is not None:
            # parent comments exists
            new_child_comment = Comment.objects.create_comment(
                user=request.user,
                path=parent_comment.get_origin,
                text=comment_text,
                photo=photo,
                parent=parent_comment
            )
            affected_users = parent_comment.get_affected_users()
            if not user == photo_creator:
                user.available_points = F('available_points') + 1
                user.total_points = F('total_points') + 1
                user.save()
            notify.send(
                request.user,
                action=new_child_comment,
                target=parent_comment,
                recipient=parent_comment.user,
                affected_users=affected_users,
                verb='replied to'
            )
            return HttpResponseRedirect(parent_comment.get_absolute_url())
        else:
            new_parent_comment = Comment.objects.create_comment(
                user=request.user,
                path=origin_path,
                text=comment_text,
                photo=photo
            )
            if not user == photo_creator:
                user.available_points = F('available_points') + 1
                user.total_points = F('total_points') + 1
                user.save()
            notify.send(
                request.user,
                action=new_parent_comment,
                target=new_parent_comment.photo,
                recipient=photo_creator,
                verb='commented'
            )
            messages.success(request,
                             "Thank you for the comment!",
                             extra_tags='safe')
            return HttpResponseRedirect(photo.get_comments_all())
    else:
        messages.error(request, "There was an error with your comment.")
        return HttpResponseRedirect(origin_path)
