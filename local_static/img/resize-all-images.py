# This script attempts to create resized copies of every non-Python (ie. *.py) 
# file in a specified directory using Pillow's *.thumbnail() method. It assumes
# that only image files and Python scripts (like this one) exist in the
# current directory.
#
# The created images are in JPEG format.
#
# If an image file size is already lower than the size_limit then the functions
# resize_1x() and resize_2x() should return and not perform any resizing 
# operations.
#
# This script is run from the command line and takes 2 arguments:
#
#   1) path/to/original/file.jpg
#   2) path/that/will/store/output/files.jpg
#
# For example:
#
#   $ python3 resize-all-images.py house-01 house-01/340kB
#
#   ... note: the 1st and 2nd arguments will have a forward slash '/' prepended
#   and appended to them so make sure to -not- include forward slashes before or
#   after the 1st and 2nd arguments.

from PIL import Image
import os, sys

size_target = 140000  # Ideal image size (in bytes)
max_iterations = 7    # Number of iterations to find optimized quality value
L = 1                 # Left pointer
R = 100               # Right pointer
quality = 50          # Starting quality value

# This resize function can be used as a sort of binary search algorithm that 
# recursively passes values to the quality parameter in order to progressively
# produce images with file sizes that approach the size_target value.
#
# Parameters:
#   file              - image file
#   name              - image file without extension
#   dimension         - (horizontal, vertical) 2-tuple size in pixels
#   dimension_factor  - factor by which in increase the dimension() tuple
#   i                 - iteration 
#   L                 - image quality from 1 to 100, max 95 per documentation,
#                       left pointer
#   https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html
#   R                 - right pointer
#
def resize_img(file, name, dimension, dimension_factor, i, quality, L, R):

  # If the size of the file (in bytes) is already below the size_target, return.
  if os.path.getsize(file_input_path + file) < size_target:
    return print("{} is already less than {} bytes".format(file, size_target))
  if i > max_iterations:
    return print("Max iterations have been reached for {}".format(file))

  # Open the image file, alter its dimensions, and save it to a new image file.
  if quality <= 95:
    im = Image.open(file_input_path + file)
    new_dimension = (dimension[0] * dimension_factor, dimension[1] * dimension_factor)
    im.thumbnail(new_dimension, Image.ANTIALIAS)
    new_prefix = '{}x-'.format(dimension_factor)
    new_name = new_prefix + name + '-' + str(dimension[0]) + '.jpg'
    im.save(file_output_path + new_name, "JPEG", quality=quality)

    # Use L and R pointers to move closer to a value for the 'quality' 
    # parameter that produces an image with a file size, in bytes, as close 
    # to size_target as possible using a binary search-type of algorithm
    if os.path.getsize(file_output_path + new_name) < size_target:
      print('Resulting image size is LESS    than {} bytes:'.format(size_target), os.path.getsize(file_output_path + new_name), 'bytes, quality =', quality)
      L = quality
      quality = int((R + L) / 2)
      resize_img(file, name, dimension, dimension_factor, i + 1, quality, L, R)
    elif os.path.getsize(file_output_path + new_name) > size_target:
      print('Resulting image size is GREATER than {} bytes:'.format(size_target), os.path.getsize(file_output_path + new_name), 'bytes, quality =', quality)
      R = quality
      quality = int((R + L) / 2)
      resize_img(file, name, dimension, dimension_factor, i + 1, quality, L, R)
    else:
      print('Resulting image size equals {} bytes:'.format(size_target), os.path.getsize(file_output_path + new_name), 'bytes, quality =', quality)
    return

# The Pillow *.thumbnail() method takes a tuple as its first argument, and it
# also maintains aspect ratio, so the resulting thumbnail's height, width, or 
# both will not exceed their respective values within the tuple (I think).
dimensions = []
def create_dimensions_list_of_tuples():
  dimensions_list = [320, 567, 768, 992, 1200, 1440]
  # dimensions_list = [320]
  for value in dimensions_list:
    dimensions.append((value, value))
create_dimensions_list_of_tuples()

# Use the Python os library's *.walk() method to look at every file in a 
# specified directory, ie. sys.argv[1]
file_input_path = './' + sys.argv[1] + '/'
file_output_path = './' + sys.argv[2] + '/'
for root, dirs, files in os.walk(file_input_path, topdown=False):
  print(root, dirs, files)
  for file in files:
    name = os.path.splitext(file)[0]
    if os.path.splitext(file)[1] != '.py':
      for dimension in dimensions:

        # Create 1x images
        try: 
          # resize_img(file, name, dimension, dimension_factor, i, quality, L, R)
          dimension_factor = 1
          print('=== Resizing: {}, {}, {}x'.format(file, dimension, dimension_factor))
          resize_img(file, name, dimension, dimension_factor, 1, quality, L, R)
        except IOError as e:
          print(repr(e), "\nError: cannot convert {} to {} - {}x".format(file, dimension, dimension_factor))
        
        # Create 2x images
        try: 
          # resize_img(file, name, dimension, dimension_factor, i, quality, L, R)
          dimension_factor = 2
          print('=== Resizing: {}, {}, {}x'.format(file, dimension, dimension_factor))
          resize_img(file, name, dimension, dimension_factor, 1, quality, L, R)
        except IOError as e:
          print(e, "Error: cannot convert {} to {} - {}x".format(file, dimension, dimension_factor))
