import re

from django import forms
from django.conf import settings
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.forms.widgets import ClearableFileInput
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _

from oby.settings.approved_universities import APPROVED_UNIVERSITIES
from oby.settings.forbidden_usernames import FORBIDDEN_USERNAMES
from oby.settings.reserved_usernames import RESERVED_USERNAMES
from .models import MyUser

# Create models here.


# For admin interface use
class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(), max_length=80)
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Verify',
                                widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'username')

    def clean_password2(self):
        password_length = settings.MIN_PASSWORD_LENGTH
        password1 = self.cleaned_data.get("password1")
        if len(password1) < password_length:
            raise forms.ValidationError(
                "Password must be longer than "
                "{} characters".format(password_length))
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# For admin interface use
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'full_name', 'bio', 'website',
                  'edu_email', 'gender', 'profile_picture', 'is_active',
                  'is_admin', 'is_verified']

    def clean_password(self):
        return self.initial["password"]


# Ready to implement
# For admin interface use
# class AdminPasswordChangeForm(forms.Form):
#     required_css_class = 'required'
#     password1 = forms.CharField(
#         label=_("Password"),
#         widget=forms.PasswordInput,
#     )
#     password2 = forms.CharField(
#         label=_("Password confirmation"),
#         widget=forms.PasswordInput,
#     )

#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super(AdminPasswordChangeForm, self).__init__(*args, **kwargs)

#     def clean_password2(self):
#         password_length = settings.MIN_PASSWORD_LENGTH
#         password1 = self.cleaned_data.get("password1")
#         if len(password1) < password_length:
#             raise forms.ValidationError(
#                 "Password must be longer than "
#                 "{} characters".format(password_length))
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2:
#             if password1 != password2:
#                 raise forms.ValidationError("Passwords do not match")
#         return password2

#     def save(self, commit=True):
#         self.user.set_password(self.cleaned_data["password1"])
#         if commit:
#             self.user.save()
#         return self.user

#     def _get_changed_data(self):
#         data = super(AdminPasswordChangeForm, self).changed_data
#         for name in self.fields.keys():
#             if name not in data:
#                 return []
#         return ['password']
#     changed_data = property(_get_changed_data)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30,
                               widget=forms.widgets.TextInput(
                                    attrs={'placeholder': 'Username'}))
    email = forms.EmailField(max_length=80,
                             widget=forms.widgets.EmailInput(
                                attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='Create password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Verify password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Verify'}))

    def clean_password2(self):
        password_length = settings.MIN_PASSWORD_LENGTH
        password1 = self.cleaned_data.get("password1")
        if len(password1) < password_length:
            raise forms.ValidationError(
                "Password must be longer than "
                "{} characters".format(password_length))
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        username_length = settings.MIN_USERNAME_LENGTH
        if username in RESERVED_USERNAMES:
            raise forms.ValidationError("Please email us to acquire this "
                                        "username: team@obystudio.com")
        elif username in FORBIDDEN_USERNAMES:
            raise forms.ValidationError("This username is not allowed. "
                                        "Please try a different one.")
        else:
            if len(username) < username_length:
                raise forms.ValidationError(
                    "Username must be longer than "
                    "{} characters".format(username_length))
            if MyUser.objects.filter(Q(username=username)).exists():
                raise forms.ValidationError("This username is already taken. "
                                            "Please try a different one.")
            if not re.match(r'^[A-Za-z0-9_]+$', username):
                raise forms.ValidationError("Sorry, but you can only have "
                                            "alphanumeric characters or _ in "
                                            "your username")
            return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if MyUser.objects.filter(
                Q(email=email)).exists():
            raise forms.ValidationError("This email is already taken. "
                                        "Please try a different one.")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(label="Username",
                               widget=forms.widgets.TextInput(
                                    attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Password'}))

    def clean_username(self):
        username = self.cleaned_data.get("username").lower()
        # if not self.user.is_active:
        #     raise forms.ValidationError("This account has been disabled")
        return username


class AccountBasicsChangeForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(), max_length=50,
                                required=False, label='Name')
    profile_picture = forms.ImageField(required=False,
                                       widget=ClearableFileInput(
                                            attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(), max_length=80)
    edu_email = forms.EmailField(widget=forms.widgets.EmailInput(),
                                 label="University email", max_length=80,
                                 required=False,
                                 help_text='Allows you to upload to the '
                                 'UNIVERSITY category.')
    bio = forms.CharField(required=False, max_length=200,
                          widget=forms.Textarea(
                                attrs={"style": "height: 5em;"}))
    website = forms.CharField(widget=forms.TextInput(), required=False,
                              max_length=90)

    class Meta:
        model = MyUser
        fields = ['username', 'profile_picture', 'full_name', 'email',
                  'edu_email', 'gender', 'bio', 'website']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AccountBasicsChangeForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"].lower()
        username_length = settings.MIN_USERNAME_LENGTH
        if username in RESERVED_USERNAMES:
            raise forms.ValidationError("Please email us to acquire this "
                                        "username: team@obystudio.com")
        elif username in FORBIDDEN_USERNAMES:
            raise forms.ValidationError("This username is not allowed. "
                                        "Please try a different one.")
        else:
            if len(username) < username_length:
                raise forms.ValidationError(
                    "Username must be longer than "
                    "{} characters".format(username_length))
            if MyUser.objects.filter(
                    Q(username=username) & ~Q(id=self.user.id)).exists():
                raise forms.ValidationError("This username is already taken. "
                                            "Please try a different one.")
            if not re.match(r'^[A-Za-z0-9_]+$', username):
                raise forms.ValidationError("Sorry, but you can only have "
                                            "alphanumeric characters or _ in "
                                            "your username")
            return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if MyUser.objects.filter(
                Q(email=email) & ~Q(id=self.user.id)).exists():
            raise forms.ValidationError("This email is already taken. "
                                        "Please try a different one.")
        return email

    def clean_edu_email(self):
        edu_email = self.cleaned_data.get('edu_email').lower()
        if MyUser.objects.filter(
                Q(edu_email=edu_email) & ~Q(id=self.user.id)).exists():
            raise forms.ValidationError("This email is already taken. \
                                        Please try a different one.")
        # Use for .edu emails
        if edu_email:
            username, domain = edu_email.split('@')

            if not domain.endswith('.edu'):
                raise forms.ValidationError(
                    "Please use a valid university email.")
            if domain not in APPROVED_UNIVERSITIES:
                raise forms.ValidationError(
                    "Sorry, this university isn't registered with us yet. "
                    "Email us to get it signed up! universities@obystudio.com")

            return edu_email


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Old password'}))
    password1 = forms.CharField(label='New password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'New password'}))
    password2 = forms.CharField(label='Verify',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Password again'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                "Your old password was entered incorrectly. "
                "Please enter it again.")
        return old_password

    def clean_password2(self):
        password_length = settings.MIN_PASSWORD_LENGTH
        password1 = self.cleaned_data.get("password1")
        if len(password1) < password_length:
            raise forms.ValidationError(
                "Password must be longer than "
                "{} characters".format(password_length))
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
        return password2


class SetPasswordForm(forms.Form):
    password1 = forms.CharField(label='New password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'New password'}))
    password2 = forms.CharField(label='Verify',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Password again'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password_length = settings.MIN_PASSWORD_LENGTH
        password1 = self.cleaned_data.get("password1")
        if len(password1) < password_length:
            raise forms.ValidationError(
                "Password must be longer than "
                "{} characters".format(password_length))
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password2'])
        if commit:
            self.user.save()
        return self.user


# Need to fix the from_email to send from a set email, not jphalisnj
class ResetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.widgets.EmailInput(
                                attrs={'placeholder': 'Email'}))

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name):
        subject = subject_template_name
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        email_message = EmailMultiAlternatives(subject, body,
                                               from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name,
                                                 context)
            email_message.attach_alternative(html_email, 'text/html')
        email_message.send()

    def get_users(self, email):
        active_users = MyUser._default_manager.filter(
            email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def save(self, subject_template_name='OBY Account Password Reset',
             email_template_name='accounts/settings/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email='team@obystudio.com', request=None,
             html_email_template_name=None):
        email = self.cleaned_data["email"].lower()
        for user in self.get_users(email):
            context = {
                'email': user.email,
                'domain': request.get_host(),
                'site_name': request.META['SERVER_NAME'],
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }

            self.send_mail(subject_template_name, email_template_name,
                           context, from_email, user.email,
                           html_email_template_name=html_email_template_name)
