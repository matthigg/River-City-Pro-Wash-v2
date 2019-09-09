# This script attempts to create resized copies of every non-Python (ie. *.py) 
# file in the current directory using Pillow's *.thumbnail() method. It assumes
# that only image files and Python scripts (like this one) exist in the
# current directory.
#
# The created images are in JPEG format.
#
# If an image file size is already lower than the size_limit then the functions
# resize_1x() and resize_2x() should return and not perform any resizing 
# operations.

from PIL import Image
import os, sys

# Ideal image size (in bytes) & number of times to run each resize function
size_target = 140000
max_iterations = 7
L = 1
R = 100
quality = 50

# This resize function can be used as a sort of binary search algorithm that 
# recursively passes values to the quality parameter in order to progressively
# produce images with file sizes that approach the size_target value.
#
# Parameters:
#   file              - image file
#   name              - image file without extension
#   dimension         - (horizontal, vertical) 2-tuple size in pixels
#   dimension_factor  - factor by which in increase the dimension() tuple
#   i                 - iterations
#   L                 - image quality from 1 to 100, max 95 per documentation,
#                       left pointer
#   https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html
#   R                 - upper bound for quality, right pointer
#
def resize_img(file, name, dimension, dimension_factor, i, quality, L, R):

  # If the size of the file (in bytes) is already below the size_target, return.
  if os.path.getsize(file) < size_target:
    return print("{} is already less than {} bytes".format(file, size_target))
  if i > max_iterations:
    return print("Max iterations have been reached for {}".format(file))

  # Open the image file, alter its dimensions, and save it to a new image file.
  if L <= 95:
    im = Image.open(file)
    new_dimension = (dimension[0] * dimension_factor, dimension[1] * dimension_factor)
    im.thumbnail(new_dimension, Image.ANTIALIAS)
    new_prefix = '{}x-'.format(dimension_factor)
    new_name = new_prefix + name + '-' + str(dimension[0]) + '.jpg'
    im.save(new_name, "JPEG", quality=quality)

    # Use L and R pointers to move closer to a value for the 'quality' 
    # parameter that produces an image with a file size, in bytes, as close 
    # to size_target as possible using a binary search-type of algorithm
    if os.path.getsize('./' + new_name) < size_target:
      print('Resulting image size is LESS than {} bytes:'.format(size_target), os.path.getsize('./' + new_name), 'bytes, quality =', quality)
      L = quality
      quality = int((R + L) / 2)
      resize_img(file, name, dimension, dimension_factor, i + 1, quality, L, R)
    elif os.path.getsize('./' + new_name) > size_target:
      print('Resulting image size is GREATER than {} bytes:'.format(size_target), os.path.getsize('./' + new_name), 'bytes, quality =', quality)
      R = quality
      quality = int((R + L) / 2)
      resize_img(file, name, dimension, dimension_factor, i + 1, quality, L, R)
    else:
      print('Resulting image size equals {} bytes:'.format(size_target), os.path.getsize('./' + new_name), 'bytes, quality =', quality)
    return

# sizes = [(320, 320), (567, 567), (768, 768), (992, 992), (1200, 1200), (1440, 1440)]
dimensions = [(567, 567)]

for root, dirs, files in os.walk('.', topdown=False):
  for file in files:
    name = os.path.splitext(file)[0]
    if os.path.splitext(file)[1] != '.py':
      for dimension in dimensions:
        try: 
          # resize_img(file, name, dimension, dimension_factor, i, quality, L, R)
          resize_img(file, name, dimension, 2, 1, quality, L, R)
        except IOError as e:
          print(e, "Error: cannot convert {} to {}x.".format(file, dimension_factor))
