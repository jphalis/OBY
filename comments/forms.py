from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Add a comment"})
    )

    def __init__(self, data=None, files=None, **kwargs):
        super(CommentForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Add Comment',
                              css_class='submit-btn go-btn',))
