# import package
from core.Ocr import Ocr
from core.Operations import Operations
import cv2
# create OCR instance
x = Ocr()
data1 = x.get_data('products','products')
data2 = x.get_data('all','all')
x.load_spellings(data2)
x.set_image('images/first.jpg')
annotations = x.text_detection()

cropped  = x.get_roi(annotations, data2, data1)
cv2.imwrite("{}.png".format('temp'), cropped)
# cv2.imshow('marked',image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
