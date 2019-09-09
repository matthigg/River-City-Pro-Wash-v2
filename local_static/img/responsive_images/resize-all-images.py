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
size_target = 150000
max_iterations = 2

# This resize function can be used as a sort of binary search algorithm that 
# recursively passes values to the quality parameter in order to progressively
# produce images with file sizes that approach the size_target value.
def resize_1x(file, name, dimension, i, quality=50):

  # If the size of the file (in bytes) is already below the size_target, return.
  if os.path.getsize(file) < size_target:
    return print("{} is already less than {}".format(file, size_target))

  # Open the image file, alter its dimensions, and save it to a new image file.
  im = Image.open(file)
  im.thumbnail(dimension, Image.ANTIALIAS)
  new_1x_name = name + '-' + str(dimension[0]) + '.jpg'
  im.save('x-' + new_1x_name, "JPEG", quality=quality)

  # Determine whether or not to continue to resize the image.
  if os.path.getsize('./' + 'x-' + new_1x_name) < size_target and i < max_iterations:
    print('Resulting image size is LESS than {} bytes:'.format(size_target), os.path.getsize('./' + 'x-' + new_1x_name))
    resize_1x(file, name, dimension, i + 1)
  elif os.path.getsize('./' + 'x-' + new_1x_name) > size_target and i < max_iterations:
    print('Resulting image size is GREATER than {} bytes:'.format(size_target), os.path.getsize('./' + 'x-' + new_1x_name))
    resize_1x(file, name, dimension, i + 1)
  else:
    print('Resulting image size equals {} bytes or max_iterations has been reached:'.format(size_target), os.path.getsize('./' + 'x-' + new_1x_name))
  return

# sizes = [(320, 320), (567, 567), (768, 768), (992, 992), (1200, 1200), (1440, 1440)]
dimensions = [(320, 320), (567, 567)]

for root, dirs, files in os.walk('.', topdown=False):
  for file in files:
    name = os.path.splitext(file)[0]
    if os.path.splitext(file)[1] != '.py':
      for dimension in dimensions:
        try: 
          resize_1x(file, name, dimension, 1)
        except IOError as e:
          print(e, "Error: cannot convert", file, "to 1x")
        
