import re
from ..spells import Checker
from ..utils import Utils
from fuzzywuzzy import fuzz


class Helpers(object):
    text_props = {}

    @classmethod
    def probable_gst(cls, word):
        if len(word) > 12:
            word = word.strip()
            d = a = 0
            for ch in word:
                if ch.isdigit():
                    d = d + 1
                elif ch.isalpha():
                    a = a + 1
                if d >= 4 and a >= 5:
                    return True
        return False

    @classmethod
    def get_props(cls, annotations):
        cls.text_props = {}
        times = 1
        # print(self.all_text)
        for obj in annotations:
            text = Checker.spell_check(obj.description)
            vertice = obj.bounding_poly.vertices
            if text:
                if text in cls.text_props.keys():
                    while True:
                        times = times + 1
                        added = text + '({})'.format(times)
                        if added not in cls.text_props.keys():
                            cls.text_props[added] = [(vertice[0].x, vertice[0].y),
                                                     (vertice[1].x, vertice[1].y),
                                                     (vertice[2].x, vertice[2].y),
                                                     (vertice[3].x, vertice[3].y)]
                            times = 1
                            break
                else:
                    cls.text_props[text] = [(vertice[0].x, vertice[0].y),
                                            (vertice[1].x, vertice[1].y),
                                            (vertice[2].x, vertice[2].y),
                                            (vertice[3].x, vertice[3].y)]
        return cls.text_props

    @classmethod
    def format_doctext(cls, doc_all_text):
        new_text = ''
        for text in doc_all_text:
            text = Utils.cleaner(text)
            text = text.upper()
            text = text.replace('.', '')
            for word in text.split(' '):
                if word:
                    word = Checker.spell_check(word)
                if word:
                    new_text = new_text + word + ' '
        formatted_text = new_text
        return formatted_text

    @classmethod
    def find_products(cls, products, doc_all_text, formatted_text):
        most = []
        less = []
        result = []
        for product in products:
            expression = ''
            for ch in product:
                expression = expression + "[\s]*" + ch
            expression = expression + '[\s]*'
            if re.findall(r'{}'.format(expression), formatted_text):
                result.append(product)
        for element in products:
            for text in doc_all_text:
                if fuzz.ratio(text, element) > 65:
                    if element not in most:
                        most.append(element)
                elif fuzz.ratio(text, element) > 10:
                    if element not in less:
                        less.append(element)
        print(most)
        print(less)
        return result