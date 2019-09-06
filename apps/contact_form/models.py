from django.db import models

class ContactForm(models.Model):
  class Meta:
    verbose_name_plural = "Contact Form" # (fix pluralization in admin panel)
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=200)
  email = models.CharField(max_length=100)
  phone = models.CharField(max_length = 24)
  message = models.TextField()