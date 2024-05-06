"""Import required modules."""
from django import forms


class ContactForm(forms.Form):
    """Contact form to send email."""
    email = forms.EmailField(label='Your Email', widget=forms.EmailInput())
    subject = forms.CharField(label='Subject', max_length=120, widget=forms.TextInput())
    content = forms.CharField(label='Message', widget=forms.Textarea)
