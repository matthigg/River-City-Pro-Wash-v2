from django.db import models

class UploadedImages(models.Model):

  # (fix pluralization in admin panel)
  class Meta:
    verbose_name_plural = "Uploaded Images" 

  Category = models.CharField(max_length=64, null=True)
  Before_Picture_Description = models.CharField(max_length=64, null=True)
  Before_Picture = models.ImageField(upload_to='images/', null=True)
  After_Picture_Description = models.CharField(max_length=64, null=True)
  After_Picture = models.ImageField(upload_to='images/', null=True)
  Notes = models.TextField(max_length = 200, null=True)
  date = models.DateTimeField(auto_now_add=True, null=True)