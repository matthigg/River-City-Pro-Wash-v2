from django.db.models import CharField, DateTimeField, ImageField, Model, TextField
from PIL import Image
import os, sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

class UploadedImages(Model):

  # Fix pluralization in admin panel
  class Meta:
    verbose_name_plural = "Uploaded Images" 

  # Define the user image input fields in the Django admin panel
  Category                    = CharField(max_length=64, null=True)
  Before_Picture_Description  = CharField(max_length=64, null=True)
  Before_Picture              = ImageField(upload_to='images/', null=True)
  After_Picture_Description   = CharField(max_length=64, null=True)
  After_Picture               = ImageField(upload_to='images/', null=True)
  date                        = DateTimeField(auto_now_add=True, null=True)
  Notes                       = TextField(max_length = 200, null=True)

  # Add some extra functionality to the default behavior of the *.save() method
  # via the *.super() method
  def save(self, *args, **kwargs):
    if self.Before_Picture:

      # Note: this will overwrite the image uploaded by the user
      self.Before_Picture = self.resize_image(self.Before_Picture)
    super(UploadedImages, self).save(*args, **kwargs)

  # Resize user-uploaded images
  # https://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file
  def resize_image(self, picture):

    # Set variables for the *.binary_search() method
    size_target = 140000  # Ideal image size (in bytes)
    dimensions = [(768, 768)]
    dimension_factor = 1
    i = 1                 # Iteration starting point
    max_i = 7             # Max number of iterations 
    quality = 50          # Starting quality value
    L = 1                 # Left pointer
    R = 100               # Right pointer

    # Run the binary search algorithm once for each set of dimensions you want to
    # create images at, ie. 320, 576, 768, etc. Currently there is no implementation
    # on the front-end to support more than one set of dimensions, but I'm keeping
    # the FOR loop here anyways so I know where to start if I implement multiple
    # dimensions later in order to support responsive images.
    for dimension in dimensions:
      im_buffer = self.binary_search(picture, size_target, dimension, dimension_factor, i, max_i, quality, L, R)

    # When files are uploaded in Django they are stored in a dictionary called
    # request.FILES as "UploadedFile" objects (or a subclass like 
    # InMemoryUploadedFile). We can try to grab the BytesIO object and convert it
    # back into a File object (or "Django" File object) while the BytesIO object
    # is in memory, ie. while it exists within this function.
    #
    # picture.name: *.name is a Django File object attribute that includes the
    # name of the file plus its relative path from MEDIA_ROOT
    # 
    # im_buffer.tell: *.tell() is an io.IOBase class method that returns
    # the current stream position, ie. where the cursor is in an open file (I 
    # think), which I guess basically tells you the size of the file if the 
    # current stream position is at the end of the file
    # 
    # Syntax:
    # InMemoryUploadedFile(file, field_name, name, content_type, size, charset)
    im_resized_file = InMemoryUploadedFile(im_buffer, None, picture.name, 'image/jpeg', im_buffer.getbuffer().nbytes, None)

    # print(picture.size, '\n', im, '\n', im_resized_file, '\n', im_resized_file.size(), '\n', im_buffer.tell())

    return im_resized_file

  def binary_search(self, picture, size_target, dimension, dimension_factor, i, max_i, quality, L, R, im_buffer=None):

    # If the size of the picture (in bytes) is already below the size_target, or 
    # if the maximum number of iterations has been reached, return.
    if picture.size < size_target:
      print("{} is already less than {} bytes".format(picture, size_target))
      return 
    if i > max_i:
      print("Max iterations have been reached for {}".format(picture))
      return im_buffer

    # Open the image file, alter its dimensions, and save it as a new BytesIO file
    # named 'im_buffer'.
    if quality <= 95:
      im = Image.open(picture)
      new_dimension = (dimension[0] * dimension_factor, dimension[1] * dimension_factor)
      im.thumbnail(new_dimension, Image.ANTIALIAS)
      # new_prefix = '{}x-'.format(dimension_factor)
      # new_name = new_prefix + name + '-' + str(dimension[0]) + '.jpg'
      im_buffer = BytesIO()
      im.save(im_buffer, "JPEG", quality=quality)

    # Use L and R pointers to move closer to a value for the 'quality' parameter 
    # that produces an image with a file size, in bytes, as close 
    # to size_target as possible using a binary search-type of algorithm
    if im_buffer.getbuffer().nbytes < size_target:
      print('Resulting image size is LESS    than {} bytes:'.format(size_target), im_buffer.getbuffer().nbytes, 'bytes, quality =', quality)
      L = quality
      quality = int((R + L) / 2)
      return self.binary_search(picture, size_target, dimension, dimension_factor, i + 1, max_i, quality, L, R, im_buffer)
    elif im_buffer.getbuffer().nbytes > size_target:
      print('Resulting image size is GREATER than {} bytes:'.format(size_target), im_buffer.getbuffer().nbytes, 'bytes, quality =', quality)
      R = quality
      quality = int((R + L) / 2)
      return self.binary_search(picture, size_target, dimension, dimension_factor, i + 1, max_i, quality, L, R, im_buffer)
    else:
      print('Resulting image size EQUALS {} bytes:'.format(size_target), im_buffer.getbuffer().nbytes, 'bytes, quality =', quality)
      return im_buffer