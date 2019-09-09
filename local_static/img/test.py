from PIL import Image
import os, sys

# size = (128, 128)

# infile = sys.argv[1]
# print(infile)
# outfile = os.path.splitext(infile)
# try:
#   im = Image.open(infile)
#   im.save('asdf.png', "PNG")
#   print(im.format, im)
# except IOError:
#   print("Can't create thumbnail for", infile)

for root, dirs, files in os.walk('.', topdown=False):
  # for name in files:
  #   print(os.path.join(root, name))
  # for name in dirs:
  #   print(os.path.join(root, name))