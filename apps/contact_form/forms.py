from django import forms
from .models import ContactForm

class CreateContactForm(forms.ModelForm):
  class Meta:
    model = ContactForm
    fields = [
      'name',
      'email',
      'phone',
      'message',
    ]