from idhantCV import Ocr
import cv2
# any_list_y = ['CADYPHYLATE LIQ', 'CIPROBID 250 MG TAB', 'CIPROBID 500 MG TAB', 'CIPROBID INFUSION',
#             'CYTDLOG 200mg TAB', 'DECANEUROBOL 50 INJ', 'DEXONA AMP [2ML]', 'DEXONA TAB [1*20]',
#             'MIFEGEST TAB', 'NEUROBOL CAP $', 'NEUROBOL INJ $']
any_list_y = ['CADIPHYLATE', 'CIPROBID', 'CIPROBID', 'CIPROBID INFUSION',
            'CYTDLOG', 'DECANEUROBOL', 'DEXONA', 'DEXONA]',
            'MIFEGEST', 'NEUROBOL', 'NEUROBOL','Neurobol*','IVORAL',
              ]
#
common_list = ['PRODUCT', 'PACKING', 'Op.Bal.Qty', 'Receipt','Qty','Total', 'Issue','Closing', 'Near','Expiry']

x = Ocr()
x.prepare_image('jammu.jpg')
x.compute_contents(1)
x.select_roi_y(any_list_y)
x.cropper_y('products')
x.search_col('Receipt')
# cv2.imshow('marked',image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
