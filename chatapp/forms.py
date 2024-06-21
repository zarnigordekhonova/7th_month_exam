# from django.forms import ModelForm
from django import forms
from .models import UserMessage


class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['text', 'attachment']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type a message...'}),
        }
    attachment = forms.FileField(required=False)


class EditMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }