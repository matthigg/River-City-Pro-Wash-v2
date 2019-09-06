from django.db import models

class ContactForm(models.Model):
  class Meta:
    verbose_name_plural = "Contact Form" # (fix pluralization in admin panel)
  name = models.CharField(max_length=64)
  address = models.CharField(max_length=200, null=True)
  email = models.CharField(max_length=64)
  phone = models.CharField(max_length = 24)
  message = models.TextField(max_length = 500)
  date = models.DateTimeField(auto_now_add=True, null=True)