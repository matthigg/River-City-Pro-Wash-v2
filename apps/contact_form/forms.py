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
      'email',
      'phone',
      'message',
    ]
    widgets = {
      'name': TextInput(attrs={'placeholder': 'name'}),
      'email': TextInput(attrs={'placeholder': 'email'}),
      'phone': TextInput(attrs={'placeholder': 'phone'}),
      'message': Textarea(attrs={
        'placeholder': 'message',
        'rows': 6,
        'cols': 40,
        }),
    }