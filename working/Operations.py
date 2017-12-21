
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
            try:
                err.replace(err.suggest()[0])
            except IndexError:
                continue
        return checker.get_text()

    # loads the data from the respective json file [params yet to be decided]
    def __load_data(self,data_name):
        s = ''
        # with open('data/{}.json'.format(data_name)) as data_file:
        #     data = json.load(data_file)
        #     print(data_file)
        print(data_name)
        with open('data/{}.json'.format(data_name)) as fh:
            data = json.load(fh)
        print("hello")
        for word in data['{}'.format(data_name.split('.')[0])]:
            s = s + word
        print(data)
        return s

    def get_products(self,blocks):
        p = []
        words = ''
        for block in blocks:
            words = words + block.description + " "
        ch_words = self.__spell_check(words, 'all')
        products = self.__load_data('products')
        for word in ch_words.split():
            if word in products.split():
                p.append(word)
        return products



