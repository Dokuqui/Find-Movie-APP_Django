"""Import required modules."""
from django import forms


class ContactForm(forms.Form):
    """Contact form to send email."""
    email = forms.EmailField(label='Your Email')
    subject = forms.CharField(label='Subject', max_length=120)
    content = forms.CharField(label='Message', widget=forms.Textarea)
