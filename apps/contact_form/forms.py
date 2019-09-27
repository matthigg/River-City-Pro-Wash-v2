from django.forms import ModelForm, TextInput, Textarea
from .models import ContactForm

class BaseForm(ModelForm):
  def __init__(self, *args, **kwargs):
    kwargs.setdefault('label_suffix', '')  
    super(BaseForm, self).__init__(*args, **kwargs)
ModelForm = BaseForm

class CreateContactForm(ModelForm):
  class Meta:
    model = ContactForm
    fields = [
      'name',
      'address',
      'email',
      'phone',
      'message',
    ]
    widgets = {
      'name': TextInput(attrs={'placeholder': 'name', 'aria-required': 'true'}),
      'address': TextInput(attrs={'placeholder': 'address', 'aria-required': 'true'}),
      'email': TextInput(attrs={'placeholder': 'email', 'aria-required': 'true'}),
      'phone': TextInput(attrs={'placeholder': 'phone', 'aria-required': 'true'}),
      'message': Textarea(attrs={
        'placeholder': 'message',
        'rows': 3,
        'cols': 40,
        'aria-required': 'true',
        }),
    }