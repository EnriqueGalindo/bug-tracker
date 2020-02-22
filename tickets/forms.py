from django import forms
from custom_user.models import MyCustomUser
from .models import Ticket


class TicketForm(forms.Form):
    title = forms.CharField(max_length=20)
    description = forms.CharField(widget=forms.Textarea)


class EditTicket(forms.Form):
    title = forms.CharField(max_length=20)
    description = forms.CharField(widget=forms.Textarea)
    assigned_to = forms.ModelChoiceField(queryset=MyCustomUser.objects.all())
