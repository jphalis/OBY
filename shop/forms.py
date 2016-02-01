from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Product
from .widgets import DateTimeWidget


DateTimeOptions = {
    'showMeridian': True
}


class ProductCreateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Coupon Title'}),
        max_length=120, label="Coupon Title"
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control',
               'placeholder': 'About this coupon',
               'style': 'height: 6em;'}),
        max_length=140, required=False
    )
    cost = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Point value cost (enter an integer)'}),
        min_value=0
    )
    promo_code = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Promotional code'}),
        max_length=30, label="Promotional Code"
    )
    list_date_start = forms.DateTimeField(widget=DateTimeWidget(
        attrs={'class': 'form-control',
               'placeholder': 'Please click the calendar on the right'},
        usel10n=True, bootstrap_version=3, options=DateTimeOptions)
    )

    class Meta:
        model = Product
        fields = ('title', 'description', 'cost', 'promo_code',
                  'list_date_start',)

    def __init__(self, data=None, files=None, **kwargs):
        super(ProductCreateForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.add_input(Submit('submit', 'Create',
                              css_class='btn btn-success',))
