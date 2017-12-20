import cv2
from enchant import DictWithPWL
from enchant.checker import SpellChecker
import json

class Operations:
    def __init__(self):
        pass

    def __spell_check(self,words, data_name):
        text = self.__load_data(data_name)
        dictionary = DictWithPWL("en_US", text)
        checker = SpellChecker(dictionary)
        checker.set_text(words)
        for err in checker:
            print(err.word)
            err.replace(err.suggest()[0])
        return checker.get_text()

    # loads the data from the respective json file [params yet to be decided]
    def __load_data(self,data_name):
        s = ''
        with open('data/{}.json'.format(data_name)) as data_file:
            data = json.load(data_file)
        for word in data['{}'.format(data_name)]:
            s = s + word
        return s

    def get_products(self,blocks):
        p = []
        for block in blocks:
            words = words + block.description + " "
        ch_words = self.__spell_check(words, 'all')
        products = self.__load_data('products')
        for word in ch_words.split():
            if word in products.split():
                p.append(word)
        return p



