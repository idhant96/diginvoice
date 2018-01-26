from core.texts import Text
from core.ocr import Ocr
from core.utils import Utils
from core.spells import Checker
import sys

all = Utils.get_data('data/all', 'all')
Checker.load_spellings(all)

products = Utils.get_data('data/products', 'products')
path = sys.argv[1]
_, doc_all_text = Ocr.document_detection(path)
print(doc_all_text)
results = Text.get_gst_dlno_date(path, doc_all_text)
fproducts = Text.get_products_image(products, doc_all_text)

print(results)
print()
print(fproducts)