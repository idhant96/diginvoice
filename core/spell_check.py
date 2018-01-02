from enchant import DictWithPWL
from enchant.checker import SpellChecker
import enchant
from core import Ocr

class SpellCheck:
    def __init__(self):
        self.dic = None
        self.dictionary = None
        self.personal = None
        self.checker = None

    def load_spellings(self, data):
        print('spells loading')
        self.dic = data
        self.dictionary = DictWithPWL("en_US")
        self.checker = SpellChecker(self.dictionary)
        self.personal = enchant.Dict()
        # Adding the personal words to dict
        for element in data:
            self.personal.add(element)

    def __spell_check(self, e_word):
        # print('spell checking of ', e_word)
        e_word = self.__cleaner(e_word)
        if e_word:
            self.checker.set_text(e_word)
            if self.checker.check(e_word) is False:
                if self.personal.check(e_word) is False:
                    if self.personal.suggest(e_word) != []:
                        # print(self.personal.suggest(e_word)[0])
                        for element in self.dic:
                            if element == self.personal.suggest(e_word)[0]:
                                print('changed')
                                return element
                    return None
        else:
            return None
        return e_word