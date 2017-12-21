# import OCR file
from working.Ocr import Ocr
from working.Operations import Operations
# import open cv version 3
import cv2

# import json
import json
#
# # get list of products
# with open('./data/products.json') as product_file:
#     products = json.load(product_file)['products']
#
#
# # get table headers
# with open('./data/headers.json') as product_file:
#     common_list = json.load(open('data/headers.json'))['table']

# create OCR instance
x = Ocr()
y = Operations()
x.set_image('images/janata.jpg')
blocks = x.text_detection()
print(y.get_products(blocks))
# cv2.imshow('marked',image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
