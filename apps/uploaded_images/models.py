from django.db.models import CharField, DateTimeField, ImageField, IntegerField, Model, TextField
from PIL import Image
import os, sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

class UploadedImages(Model):

  # Fix pluralization in admin panel
  class Meta:
    verbose_name_plural = "Uploaded Images" 

  # Define image categories to be displayed under in ~/templates/our-work.html
  CATEGORIES = (
    ('No_Category', 'Select a Category'),
    ('Concrete_and_Brick', 'Concrete & Brick'),
    ('Decks', 'Decks'),
    ('Deck_Staining', 'Deck Staining'),
    ('Driveways', 'Driveways'),
    ('Fences', 'Fences'),
    ('Graffiti_Removal', 'Graffiti Removal'),
    ('Houses', 'Houses'),
    ('Sidewalks', 'Sidewalks'),
  )

  # Define the user image input fields in the Django admin panel
  Category                      = CharField(max_length=64, null=True, choices=CATEGORIES, default='None')
  Before_Picture_Description    = CharField(max_length=64, null=True, blank=True)
  Before_Picture_Size_kB        = IntegerField(null=True, default=140)
  Before_Picture_Max_Dimension  = IntegerField(null=True, default=768)
  Before_Picture                = ImageField(upload_to='images/', null=True)
  After_Picture_Description     = CharField(max_length=64, null=True, blank=True)
  After_Picture_Size_kB         = IntegerField(null=True, default=140)
  After_Picture_Max_Dimension   = IntegerField(null=True, default=768)
  After_Picture                 = ImageField(upload_to='images/', null=True)
  date                          = DateTimeField(auto_now_add=True, null=True)
  Notes                         = TextField(max_length = 200, null=True, blank=True)

  # Add some extra functionality to the default behavior of the *.save() method
  # via the *.super() method
  def save(self, *args, **kwargs):
    if self.Before_Picture:

      # Note: this will overwrite the image uploaded by the user
      self.Before_Picture = self.resize_image(self.Before_Picture, self.Before_Picture_Size_kB, self.Before_Picture_Max_Dimension)
      self.After_Picture = self.resize_image(self.After_Picture, self.After_Picture_Size_kB, self.After_Picture_Max_Dimension)
    super(UploadedImages, self).save(*args, **kwargs)

  # Resize user-uploaded images
  # https://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file
  def resize_image(self, picture, size_target, max_dim):

    # Set variables for the *.binary_search() method
    size_target = size_target * 1000   # Ideal image size (in bytes)
    dimensions = [(max_dim, max_dim)]  # Dimensions for *.thumbnail() 
    dimension_factor = 1      # For generating 1x, 2x (retina), or higher res.
    i = 1                     # Iteration starting point
    max_i = 7                 # Max number of iterations 
    quality = 50              # Starting quality value
    L = 1                     # Left pointer
    R = 100                   # Right pointer

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
    # Syntax:
    # InMemoryUploadedFile(file, field_name, name, content_type, size, charset)
    im_resized_file = InMemoryUploadedFile(im_buffer, None, picture.name, 'image/jpeg', im_buffer.getbuffer().nbytes, None)
    return im_resized_file

  # Binary search algorithm that uses 3 pointers -- L, R, and quality, where the
  # value for quality is used by PIL's *.save() method to set the quality of an
  # image -- in an attempt to find a quality that produces an image with an file
  # size that is as close to the value for size_target as max_i number of
  # iterations will allow (close, but not perfect, could be memoized I think).
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
      # that produces an image with a file size, in bytes, as close to size_target
      # as possible using a binary search-type of algorithm.
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
    else:
      return im_buffer