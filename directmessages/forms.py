# from django import forms

# from .models import DirectMessage

# # Create forms here.


# class ComposeForm(forms.ModelForm):
#     body = forms.CharField(
#         widget=forms.Textarea(
#             attrs={'placeholder': 'Type your message here!',
#                    'style': 'height: 6em;'}
#         )
#     )

#     class Meta:
#         model = DirectMessage
#         fields = ('recipient', 'body', 'image')


# class ReplyForm(forms.ModelForm):
#     body = forms.CharField(
#         widget=forms.Textarea(
#             attrs={'placeholder': 'Type your message here!',
#                    'style': 'height: 6em;'}
#         )
#     )

#     class Meta:
#         model = DirectMessage
#         fields = ('body', 'image')
