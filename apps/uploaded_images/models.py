from django.db import models

class UploadedImages(models.Model):

  # (fix pluralization in admin panel)
  class Meta:
    verbose_name_plural = "Uploaded Images" 

  img_name = models.CharField(max_length=100)
  img_alt = models.CharField(max_length=64)
  img_category = models.CharField(max_length=64, null=True)
  img_notes = models.CharField(max_length=200, null=True)
  img_file = models.ImageField(upload_to='images/', null=True)