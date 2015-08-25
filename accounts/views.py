from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import (get_object_or_404, HttpResponseRedirect,
                              redirect, render)
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_http_methods

# from analytics.signals import page_view
from notifications.signals import notify
from photos.models import Photo

from .forms import (AccountBasicsChangeForm, LoginForm, PasswordChangeForm,
                    RegisterForm, ResetPasswordForm, SetPasswordForm)
from .models import Follower, MyUser

# Create your views here.


@login_required
@cache_page(60 * 2)
def profile_view(request, username):
    user = get_object_or_404(MyUser, username=username)

    if user.username == "anonymous":
        return render(request, "accounts/anonymous.html", {})
    else:
        photos = Photo.objects.select_related(
                'category', 'creator').filter(creator=user)[:150]

        try:
            follow = Follower.objects.get(user=user)
        except Follower.DoesNotExist:
            follow = None

        # page_view.send(
        #     user,
        #     page_path=request.get_full_path(),
        # )

        context = {
            'follow': follow,
            'photos': photos,
            'user': user
        }
        return render(request, "accounts/profile_view.html", context)


@cache_page(60 * 4)
def followers_thread(request, username):
    try:
        user = MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        raise Http404
    followers_set = Follower.objects.filter(user=user.id)
    return render(request, "accounts/followers_thread.html",
                  {'followers_set': followers_set})


@cache_page(60 * 4)
def following_thread(request, username):
    try:
        user = MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        raise Http404
    following_set = Follower.objects.filter(user=user.id)
    return render(request, "accounts/following_thread.html",
                  {"following_set": following_set})


@login_required
@require_http_methods(['POST'])
def follow_ajax(request):
    follower, created = Follower.objects.get_or_create(user=request.user)
    user_id = request.POST.get('user_id')
    user = get_object_or_404(MyUser, id=user_id)

    followed, created = Follower.objects.get_or_create(user=user)

    try:
        user_followed = Follower.objects.get(user=user, followers=follower)
    except Follower.DoesNotExist:
        user_followed = None

    if user_followed:
        followed.followers.remove(follower)
        viewer_has_followed = False
    else:
        followed.followers.add(follower)
        viewer_has_followed = True

        notify.send(
            request.user,
            recipient=user,
            verb='is now supporting you'
        )

    followed.save()
    user.save()

    data = {
        "viewer_has_followed": viewer_has_followed,
        "followers_count": followed.followers.count()
    }
    return JsonResponse(data)


@login_required
@cache_page(60)
def account_settings(request):
    user = request.user
    account_change_form = AccountBasicsChangeForm(request.POST or None,
                                                  request.FILES or None,
                                                  instance=user, user=user)

    if request.method == 'POST':
        if account_change_form.is_valid():
            username = account_change_form.cleaned_data['username']
            email = account_change_form.cleaned_data['email']

            account_change_form.username = username
            account_change_form.email = email

            account_change_form.save()
            messages.success(request,
                             "You have successfully updated your profile.")

    context = {
        'account_change_form': account_change_form
    }
    return render(request, 'accounts/settings/account_settings.html', context)


@sensitive_post_parameters()
@login_required
def password_change(request):
    form = PasswordChangeForm(request.POST or None, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            password = form.cleaned_data['password2']
            current_user = form.user
            current_user.set_password(password)
            current_user.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,
                             "You have successfully changed your password.")
    return render(request, 'accounts/settings/password_change.html',
                  {'form': form})


@cache_page(60 * 10)
def password_reset(request,
                   template_name='accounts/settings/password_reset_form.html',
                   email_template_name='accounts/settings/password_reset_email.html',
                   subject_template_name='OBY Account Password Reset',
                   password_reset_form=ResetPasswordForm,
                   token_generator=default_token_generator,
                   from_email='team@obystudio.com',
                   html_email_template_name=None):
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            form.save(**opts)
            messages.success(request,
                             "If that email is registered to an account, \
                             instructions for resetting your password \
                             will be sent soon. Please make sure to check \
                             your junk email/spam folder if you do not \
                             receive an email.")
    else:
        form = password_reset_form()
    return render(request, template_name, {'form': form})


@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           token_generator=default_token_generator):
    assert uidb64 is not None and token is not None
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        form = SetPasswordForm(request.POST or None, user=user)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("login"))
    else:
        validlink = False
        form = None
        messages.error(request, "Password reset unsuccessful")
    context = {
        'form': form,
        'validlink': validlink
    }
    return render(request, 'accounts/settings/password_set.html', context)


def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


@cache_page(60 * 10)
def auth_login(request):
    if request.user.is_authenticated():
        return redirect("home")
    else:
        form = LoginForm(request.POST or None)
        next_url = request.GET.get('next')

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                if next_url is not None:
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect(reverse("home"))
            else:
                messages.warning(request, "Username or password is incorrect.")
        action_url = reverse("login")
        title = "Sign in"
        submit_btn = title
        context = {
            "form": form,
            "action_url": action_url,
            "title": title,
            "submit_btn": submit_btn
        }
        return render(request, "visitor/login_register.html", context)


@cache_page(60 * 10)
def auth_register(request):
    if request.user.is_authenticated():
        return redirect("home")
    else:
        form = RegisterForm(request.POST or None)
        next_url = request.GET.get('next')

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            new_user = MyUser()
            new_user.username = username
            new_user.email = email
            new_user.set_password(password)
            new_user.save()
            user = authenticate(username=username, password=password)

            if user is not None:
                admin = MyUser.objects.get(username='oby')
                thank_you_message = "Thank you for signing up!"

                notify.send(
                    admin,
                    recipient=user,
                    verb=thank_you_message
                )

                login(request, user)

                if next_url is not None:
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect(reverse("home"))
        action_url = reverse("register")
        title = "Register"
        submit_btn = "Create account"

        context = {
            "form": form,
            "action_url": action_url,
            "title": title,
            "submit_btn": submit_btn
        }
        return render(request, "visitor/login_register.html", context)
