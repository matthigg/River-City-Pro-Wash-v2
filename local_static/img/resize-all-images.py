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
i = 1                 # Starting iteration (1-indexed instead of 0-indexed)
max_iterations = 7    # Number of iterations to find optimized quality value
L = 1                 # Left pointer
R = 100               # Right pointer
quality = 50          # Starting quality value

# The Pillow *.thumbnail() method takes a tuple as its first argument, and it
# also maintains aspect ratio, so the resulting thumbnail's height, width, or 
# both will not exceed their respective values within the tuple.
# dimensions_blur = [50]
# dimensions_blur_tuples = []
# dimensions_1x = [320, 576, 768, 992, 1200, 1440]
dimensions_1x = [320, 576, 768]
dimensions_1x_tuples = []
dimensions_2x = [320, 576, 768]
dimensions_2x_tuples = []
def create_dimensions_list_of_tuples(dimensions, dimensions_tuples):
  for value in dimensions:
    dimensions_tuples.append((value, value))
# create_dimensions_list_of_tuples(dimensions_blur, dimensions_blur_tuples)
create_dimensions_list_of_tuples(dimensions_1x, dimensions_1x_tuples)
create_dimensions_list_of_tuples(dimensions_2x, dimensions_2x_tuples)

# This resize function can be used as a sort of binary search algorithm that 
# recursively passes values to the quality parameter in order to progressively
# produce images with file sizes that approach the size_target value.
#
# Parameters:
#   file              - image file
#   name              - image file without extension
#   dimension         - (horizontal, vertical) 2-tuple size in pixels
#   dimension_factor  - factor by which in increase the dimension() tuple
#   ext               - file extension as a tuple, ie. ('.jpg', 'JPEG')
#   i                 - iteration 
#   L                 - image quality from 1 to 100, max 95 per documentation,
#                       left pointer
#   https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html
#   R                 - right pointer
#
def resize_img(file, name, dimension, dimension_factor, file_ext, file_ext_alias, i, quality, L, R):

  # If the size of the file (in bytes) is already below the size_target, or if
  # the maximum number of iterations has been reached, return.
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
    new_name = new_prefix + name + '-' + str(dimension[0]) + file_ext
    im.save(file_output_path + new_name, file_ext_alias, quality=quality)

    # Use L and R pointers to move closer to a value for the 'quality' 
    # parameter that produces an image with a file size, in bytes, as close 
    # to size_target as possible using a binary search-type of algorithm
    if os.path.getsize(file_output_path + new_name) < size_target:
      print('Resulting image size is LESS    than {} bytes:'.format(size_target), os.path.getsize(file_output_path + new_name), 'bytes, quality =', quality)
      L = quality
      quality = int((R + L) / 2)
      resize_img(file, name, dimension, dimension_factor, file_ext, file_ext_alias, i + 1, quality, L, R)
    elif os.path.getsize(file_output_path + new_name) > size_target:
      print('Resulting image size is GREATER than {} bytes:'.format(size_target), os.path.getsize(file_output_path + new_name), 'bytes, quality =', quality)
      R = quality
      quality = int((R + L) / 2)
      resize_img(file, name, dimension, dimension_factor, file_ext, file_ext_alias, i + 1, quality, L, R)
    else:
      print('Resulting image size equals {} bytes:'.format(size_target), os.path.getsize(file_output_path + new_name), 'bytes, quality =', quality)
    return

def create_resized_img(file, name, dimension, dimension_factor, file_ext, file_ext_alias, i, quality, L, R):
  try: 
    print('=== Resizing: {}, {}, {}, {}x'.format(file, dimension, file_ext, dimension_factor))
    resize_img(file, name, dimension, dimension_factor, file_ext, file_ext_alias, i, quality, L, R)
  except IOError as e:
    print(e, "\nError: cannot convert {} to {} {}- {}x".format(file, dimension, file_ext, dimension_factor))

# Use the Python os library's *.walk() method to look at every file in a specified
# directory in order to pass those files to the resize_img() function, and take the
# output from that function and save them to another directory. This script
# assumes that all of the files in the sys.argv[1] directory, including sub-
# directories, are images.
# 
# Parameters:
#   file_input_path     - location to being os.walk()'ing, also searches 
#                         subdirectories
#   file_output_path    - save the results from the resize_img() function here
#
file_input_path = './' + sys.argv[1] + '/'
file_output_path = './' + sys.argv[2] + '/'
for root, dirs, files in os.walk(file_input_path, topdown=False):
  for file in files:
    name = os.path.splitext(file)[0]
    if os.path.splitext(file)[1] != '.py':

      # Parameters:
      #   dimension_factor - integer used to multiply dimensions, specifically
      #                      meant to create images for retina displays
      #   file_ext         - image file extension for newly created files,
      #                      ie. '.jpg'
      #   file_ext_alias   - image file extension alias used by PIL's *.save() 
      #                      method, ie. 'JPEG'
      #
      # Syntax:
      # resize_img(file, name, dimension, dimension_factor, ext, i, quality, L, R)

      # Call the create_resized_img() function, specifying arguments to pass to
      # the dimension_factor, file_ext, file_ext_alias parameters.
      #
      # Syntax:
      # create_resized_img(file, name, dimension, dimension_factor, file_ext, file_ext_alias, i, quality, L, R)
      
      # This FOR loop iterates over a list of tuples defined somehwere earlier in 
      # this script that is generated by the create_dimensions_list_of_tuples() 
      # function. Since the dimensions of the images that are eventually produced
      # aren't set in stone, these parts of the script is mostly controlled by hand.
      # for dimension in dimensions_blur_tuples:

      # Create a low-quality/blurred placeholder image
      # for dimension in dimensions_blur_tuples:
      #   create_resized_img(file, name, dimension, 1, '.jpg', 'JPEG', i, quality, L, R)

      # Create 1x JPEG and WEBP images
      for dimension in dimensions_1x_tuples:
        create_resized_img(file, name, dimension, 1, '.jpg', 'JPEG', i, quality, L, R)
        create_resized_img(file, name, dimension, 1, '.webp', 'WEBP', i, quality, L, R)

      # Create 2x JPEG and WEBP images
      for dimension in dimensions_2x_tuples:
        create_resized_img(file, name, dimension, 2, '.jpg', 'JPEG', i, quality, L, R)
        create_resized_img(file, name, dimension, 2, '.webp', 'WEBP', i, quality, L, R)
