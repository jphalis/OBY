from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView

from accounts.models import MyUser
from core.mixins import LoginRequiredMixin

# Create your views here.


class SearchListView(LoginRequiredMixin, ListView):
    model = MyUser
    template_name = 'search/search_results.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchListView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        user_qs = super(SearchListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')

        if query:
            user_qs = self.model.objects.filter(
                Q(username__icontains=query)
                )
            # adds multiple filters to the queryset
            # user_qs = self.model.objects.filter(
            #     Q(username__icontains=query) |
            #     Q(username__startswith=query)
            #     )
        return user_qs


@login_required
@require_http_methods(['GET'])
def search_ajax(request):
    q = request.GET.get('q')
    data = {}

    if q:
        users = MyUser.objects.filter(username__icontains=q)
        data = [{'username': user.username} for user in users]
    return JsonResponse(data, safe=False)
