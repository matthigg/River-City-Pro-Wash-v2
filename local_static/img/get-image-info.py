from PIL import Image
import os, sys

im = Image.open(sys.argv[1])
print(im, os.path.getsize('./' + sys.argv[1]))