from enchant import DictWithPWL
from enchant.checker import SpellChecker
import enchant
from fuzzywuzzy import fuzz
from ..utils import Utils


class Checker(object):
    dic = None
    checker = None
    personal = None

    @classmethod
    def load_spellings(cls, data):
        cls.dic = data
        cls.dictionary = DictWithPWL("en_US")
        cls.checker = SpellChecker(cls.dictionary)
        cls.personal = enchant.Dict()
        # Adding the personal words to dict
        for element in data:
            cls.personal.add(element)

    @classmethod
    def spell_check(cls, e_word):
        if e_word == '.':
            return None
        e_word = Utils.cleaner(e_word)
        if e_word:
            cls.checker.set_text(e_word)
            if cls.checker.check(e_word) is False:
                if cls.personal.check(e_word) is False:
                    if cls.personal.suggest(e_word) != []:
                        for suggest in cls.personal.suggest(e_word):
                            for element in cls.dic:
                                if suggest == element:
                                    return element
                    smalls = ['2ML', 'KIT']
                    for element in smalls:
                        if fuzz.ratio(e_word, element) > 0:
                            return element
                    return None
        else:
            return None
        return e_word

