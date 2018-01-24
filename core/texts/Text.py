from .Helpers import Helpers
from ..utils import Utils
import re


class Text(object):
    results = {}

    @classmethod
    def get_products_image(cls, products, doc_all_text):
        formatted_text = Helpers.format_doctext(doc_all_text)
        result = Helpers.find_products(products, doc_all_text, formatted_text)
        return result

    @classmethod
    def get_gst_dlno_date(cls, path, doc_all_text):
        cls.results["invoices"] = {}
        if path:
            result = cls.results["invoices"][path] = {}
            dlno = result["DLNO"] = {}
            gstin = result["GSTIN"] = {}
            date = result["INV DATE"] = {}
            for text in doc_all_text:
                if Helpers.probable_gst(text):
                    prob_gst = Utils.formatter(text)
                    if Utils.check_gst_format(prob_gst):
                        gstin[Utils.check_gst_format(prob_gst)] = True
                        continue
                    else:
                        prob_gst = ''.join(re.findall(r'[A-Z\d]{2}[A-Z]{5}\d{3,4}[A-Z\d]{3,4}', prob_gst))
                        prob_gst = Utils.change_gst_letters(prob_gst)
                        if Utils.check_gst_format(prob_gst):
                            gstin[Utils.check_gst_format(prob_gst)] = True
                            continue
                    # prob_gst = self.change_gst_letters(prob_gst)
                    prob_gst = ''.join(re.findall(r'[A-Z\d]{2}[A-Z]{5}\d{3,4}[A-Z\d]{3,4}', text))
                    if prob_gst:
                        prob_gst = Utils.change_gst_letters(prob_gst)
                        if Utils.check_gst_format(prob_gst):
                            gstin[prob_gst] = True
                        else:
                            gstin[prob_gst] = False

                if re.findall(r'\d+\/\d+A', text):
                    dlno[''.join(re.findall(r'\d+\/\d+[\s]*A', text))] = True
                elif re.findall(r'\d+\/\d+\/\d+', text):
                    date[''.join(re.findall(r'\d+\/\d+\/\d+', text))] = True
        return cls.results