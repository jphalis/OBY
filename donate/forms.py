from django import forms

# Create forms here.


class DonationForm(forms.Form):
    # Auto populate registered name
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Name"})
    )
    # Auto populate registered email address
    email = forms.EmailField(
        max_length=120,
        widget=forms.TextInput())
    amount = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"placeholder": "$0.00"}))
    message = forms.CharField(
        max_length=4000, required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Leave a message for us",
                   "style": "height: 6em;"})
    )
