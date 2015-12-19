from django import forms
from django.conf import settings
from django.core.files.images import get_image_dimensions

from .models import Photo


class PhotoUploadForm(forms.ModelForm):
    description = forms.CharField(
        required=False, max_length=250,
        widget=forms.Textarea(attrs={"placeholder": "What's this photo about?",
                                     "style": "height: 7em;"})
    )

    class Meta:
        model = Photo
        fields = ('photo', 'category', 'description')

    #  Use when wanting to limit who can post to certain categories
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'request'):
            self.request = kwargs.pop('request')

        super(PhotoUploadForm, self).__init__(*args, **kwargs)

        # if not self.request.user.is_scale_management:
        #     self.fields['category'].queryset = Category.objects.exclude(
        #         title='Scale Management')

        # if not self.request.user.edu_email:
        #     self.fields['category'].queryset = Category.objects.exclude(
        #         title='University')

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        try:
            w, h = get_image_dimensions(photo)
            # validate dimensions
            min_width = 80
            min_height = 80
            max_height = 1500
            if min_width > w or min_height > h:
                raise forms.ValidationError(
                    u'That image is too small. '
                    'Please choose an image that is at least '
                    '{} x {} pixels.'.format(
                        min_width, min_height))
            elif h > max_height:
                raise forms.ValidationError(
                    u'That image is too large. '
                    'Please choose an image that is smaller than '
                    '{} pixels tall.'.format(
                        max_height))
            else:
                pass

            # validate file size
            if photo.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                raise forms.ValidationError(
                    u'Image size may not exceed 5MB.')
        except AttributeError:
            pass
        return photo
