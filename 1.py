from PIL import Image
import sys
image = Image.open('{}'.format(sys.argv[1]))
image.thumbnail((360, 360), Image.ANTIALIAS)
image.save('thumbnail.jpg', 'JPEG')