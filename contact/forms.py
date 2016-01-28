from django import forms

# Create forms here.


class BusinessContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Name"})
    )
    company = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Company"})
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"placeholder": "contact@company.com"})
    )
    coupons = forms.ChoiceField(
        choices=(
            ("Yes", "Yes"),
            ("Maybe", "Maybe"),
            ("No", "No")
        ),
        initial='Yes',
        label='Are you able to contribute promotional offers?'
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Is there anything we should know?",
                   "style": "height: 6em;"})
    )
