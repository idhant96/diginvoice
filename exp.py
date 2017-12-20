# import OCR file
from core import Ocr

# import open cv version 2
import cv2

# import json
import json

# get list of products
with open('./data/products.json') as product_file:
    products = json.load(product_file)['products']


# get table headers
with open('./data/headers.json') as product_file:
    common_list = json.load(open('data/headers.json'))['table']

# create OCR instance
x = Ocr()
x.set_image('images/jammu.jpg')
blocks = x.text_detection()
x.select_roi_y(products)
x.cropper_y('products')
x.search_col('Receipt')
# cv2.imshow('marked',image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
