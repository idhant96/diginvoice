# import package
from core.Ocr import Ocr
from core.Operations import Operations
import cv2
# create OCR instance
x = Ocr()




#
# data1 = x.get_data('products','products')
# spells = x.get_data('all','all')
# x.load_spellings(spells)
x.lol('images/invoices')
# x.set_image('images/janata.jpg')
# x.text_detection()
# x.get_props()
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
