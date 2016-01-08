import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods

from accounts.models import MyUser

from .forms import ProductCreateForm
from .models import Product
from .signals import listuse_status_check

# Create your views here.


@login_required
def shop(request):
    products = Product.objects.all()

    for product in products:
        listuse_status_check.send(sender=product)

    products_listed = Product.objects.listed()
    products_useable = (Product.objects.filter(buyers=request.user)
                                       .useable()
                                       .select_related('owner')
                                       .prefetch_related('buyers'))

    context = {
        'products_listed': products_listed,
        'products_useable': products_useable
    }
    return render(request, 'shop/shop.html', context)
    # raise Http404


@login_required
@require_http_methods(['POST'])
def product_purchase(request):
    user = request.user
    u = MyUser.objects.get(username=user)
    product_pk = request.POST.get('product_pk', False)
    purchased, created = Product.objects.get_or_create(pk=product_pk)

    try:
        user_purchased = Product.objects.get(pk=product_pk, buyers=user)
    except:
        user_purchased = None

    if user_purchased:
        user_has_purchased = False
    else:
        if u.available_points >= purchased.cost or purchased.discount_cost:
            if purchased.discount_cost:
                u.update(
                    available_points=F('available_points') - purchased.discount_cost)
                # u.available_points -= purchased.discount_cost
            else:
                # u.available_points -= purchased.cost
                u.update(
                    available_points=F('available_points') - purchased.cost)

            # u.save()
            purchased.buyers.add(user)
            purchased.save()
            user_has_purchased = True
        else:
            messages.error(request,
                           "We're sorry, you do not have enough points \
                           to redeem this product.")
    user_remaining_points = float(u.available_points)
    data = {
        "user_has_purchased": user_has_purchased,
        "user_remaining_points": user_remaining_points
    }
    return JsonResponse(data)


@login_required
@cache_page(60 * 10)
def product_create(request):
    user = MyUser.objects.get(username=request.user)

    if user.is_advertiser and user.creations_allowed > 0:
        form = ProductCreateForm()

        if request.method == 'POST':
            form = ProductCreateForm(request.POST or None, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner = user
                obj.list_date_end = obj.list_date_start + datetime.timedelta(
                    days=7, hours=10)
                obj.use_date_start = obj.list_date_start
                obj.use_date_end = obj.list_date_end + datetime.timedelta(
                    days=14)
                obj.save()
                user.update(creations_allowed=F('creations_allowed') - 1)
                messages.success(request,
                                 "Thank you! You have successfully \
                                 created your coupon!")
                return HttpResponseRedirect(reverse('shop'))
            else:
                form = ProductCreateForm()

        context = {
            "form": form
        }
        return render(request, "shop/product_create.html", context)
    else:
        return HttpResponseRedirect(reverse("home"))
    # raise Http404


# def single(request, slug):
#   try:
#       product = Product.objects.get(slug=slug)
#       images = ProductImage.objects.filter(product=product)
#       context = {
#           'product': product,
#           'images': images
#       }
#       template = 'shop/single.html'
#       return render(request, template, context)
#   except:
#       raise Http404
