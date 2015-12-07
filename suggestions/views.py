# import random

# from django.shortcuts import render
# from django.views.generic import View

# from photos.models import Photo

# # Create your views here.


# # The queries are not accurate. Example purposes only
# class SuggestionView(View):
#     def get(self, request, *args, **kwargs):
#         hashtag_views = None
#         photos = None
#         top_hashtags = None
#         owned = None

#         try:
#             hashtag_views = request.user.hashtagview_set.all() \
#                 .order_by("-count")[:6]
#         except:
#             pass

#         try:
#             owned = request.user.myphotos.photos.all()
#         except:
#             pass

#         if hashtag_views:
#             top_hashtags = [x.hashtag for x in hashtag_views]
#             photos = Photo.objects.filter(hashtag__in=top_hashtags)
#             if owned:
#                 photos = photos.exclude(pk__in=owned)
#             if photos.count < 10:
#                 photos = Photo.objects.all().order_by("?")
#                 if owned:
#                     photos = photos.exclude(pk__in=owned)
#                 photos = photos[:10]
#             else:
#                 photos = photos.distinct()
#                 photos = sorted(photos, key=lambda x: random.random)

#         context = {
#             'photos': photos,
#             'top_hashtags': top_hashtags
#         }
#         return render(request, 'suggestions/suggested_photos.html', context)
