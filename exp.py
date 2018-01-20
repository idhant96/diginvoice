# import package
from core.Ocr import Ocr
import sys
from core.Operations import Operations
import cv2
# create OCR instance
x = Ocr()




#
products = x.get_data('products','products')
spells = x.get_data('all','all')
x.load_spellings(spells)
# x.lol('images/invoices/batch3')
# x.set_image('images/invoices/more/IMG_20180105_181004896.jpg')
# x.document_detection()
# x.format_doctext()
# x.get_props()
# x.get_products('images/invoices/more', products)
x.get_products_image(sys.argv[1], products)
# cropped  = x.get_roi(data1)
# cv2.imwrite("{}.png".format('temp'), cropped)
# x.set_image('temp.png')
# x.text_detection()
# x.get_props()
# x.get_rows()
# x.get_columns()
# x.map_contents()
# cv2.imshow('marked',image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
