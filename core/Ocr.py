import io
import json
from enchant import DictWithPWL
from enchant.checker import SpellChecker
import enchant
from fuzzywuzzy import fuzz

import cv2
from google.cloud import vision
from google.cloud.vision import types
import re
import os
import sys

'''
to Jay Sir
Functions needs to be distributed
'''


class Ocr:
    """
    Ocr class
    provides functions to perform different actions on image
    """

    # google vision client
    google_vision_client = vision.ImageAnnotatorClient()

    def __init__(self):
        """
        Ocr construction
        Initialize instance variables
        """
        # image path
        self.image_path = ''
        # image instance
        self.crop_hints = ['PRODUCTS','Particulars','PARTICULARS', 'DESCRIPTION', 'PRODUCT',
                           ]
        self.doc_all_text = []
        self.formatted_text = ''
        self.blocks = []
        self.index = None
        self.o_item = []
        self.image = None
        self.dictionary = None
        self.personal = None
        self.checker = None
        self.rows = {}
        self.cols = {}
        self.all_text = []
        self.contents = {}
        self.roi = []
        self.titles = []
        self.dic = None
        self.response = self.annotations = None
        self.y_min = self.y_max = self.x_min = self.x_max = 0
        self.text_props = {}

    @staticmethod
    def __resize(image):
        r = 400.0 / image.shape[1]
        dim = (300, int(image.shape[0] * r))
        # perform the actual resizing of the image and show it
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized

    @staticmethod
    def __cleaner(st):
        # print('text cleaning')
        st = st.encode('ascii', 'ignore').decode('utf-8')
        return re.sub(r'[(?|$|,+''"”*#:|!)]', r'', st)

    @staticmethod
    def get_data(file_name, obj):
        with open('data/{}.json'.format(file_name)) as fh:
            data = json.load(fh)
        return data['{}'.format(obj)]

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
        if e_word == '.':
            return None
        e_word = self.__cleaner(e_word)
        if e_word:
            self.checker.set_text(e_word)
            if self.checker.check(e_word) is False:
                if self.personal.check(e_word) is False:
                    if self.personal.suggest(e_word) != []:
                        # print(self.personal.suggest(e_word)[0])
                        for suggest in self.personal.suggest(e_word):
                            for element in self.dic:
                                if suggest == element:
                                    return element
                    smalls = ['2ML', 'KIT']
                    for element in self.dic:
                        if fuzz.ratio(e_word, element) > 65:
                            return element
                    for element in smalls:
                        if fuzz.ratio(e_word, element) > 0:
                            return element
                    return None
        else:
            return None
        return e_word

    def set_image(self, img):
        """
        set image instance with the given url
        :param img:
        :return:
        """
        self.image_path = '{}'.format(img)
        # set image instance
        self.image = cv2.imread(self.image_path,0)

    def document_detection(self):
        with io.open(self.image_path, 'rb') as image_file:
            data = image_file.read()
        vision_image = types.Image(content=data)
        response = Ocr.google_vision_client.document_text_detection(image=vision_image)
        self.annotations = response.text_annotations
        self.doc_all_text = self.annotations[0].description.split('\n')

    def text_detection(self):
        """
        detect text from the image
        :return:
        """
        # print(self.image_path)
        # format image into google vision understandable
        with io.open(self.image_path, 'rb') as image_file:
            data = image_file.read()
        vision_image = types.Image(content=data)
        # detect text
        response = Ocr.google_vision_client.text_detection(image=vision_image)
        self.annotations = response.text_annotations
        self.all_text = self.annotations[0].description.split('\n')
        # print('text detection')
        # print(self.all_text)
        # print(block_words)

    def get_props(self):
        self.text_props = {}
        times = 1
        # print(self.all_text)
        for obj in self.annotations:
            text = self.__spell_check(obj.description)
            vertice = obj.bounding_poly.vertices
            if text:
                if text in self.text_props.keys():
                    while True:
                        times = times + 1
                        added = text + '({})'.format(times)
                        if added not in self.text_props.keys():
                            self.text_props[added] = [(vertice[0].x, vertice[0].y),
                                                             (vertice[1].x, vertice[1].y),
                                                             (vertice[2].x, vertice[2].y),
                                                             (vertice[3].x, vertice[3].y)]
                            times = 1
                            break
                else:
                    self.text_props[text] = [(vertice[0].x, vertice[0].y),
                                                             (vertice[1].x, vertice[1].y),
                                                             (vertice[2].x, vertice[2].y),
                                                             (vertice[3].x, vertice[3].y)]
        # print(self.text_props)
        # return self.text_props

    def format_doctext(self):
        new_text = ''
        print(self.doc_all_text)
        for text in self.doc_all_text:
            text = self.__cleaner(text)
            text = text.upper()
            text = text.replace('.', '')
            for word in text.split(' '):
                if word:
                    word = self.__spell_check(word)
                if word:
                    new_text = new_text + word + ' '
        self.formatted_text = new_text
        print(self.formatted_text)

    def find_products(self, products):
        print(self.doc_all_text)
        result = []
        for product in products:
            expression = ''
            for ch in product:
                expression = expression + "[\s]*" + ch
            expression = expression + '[\s]*'
            if re.findall(r'{}'.format(expression), self.formatted_text):
                # print('regex result: ', product)
                result.append(product)
        # print(text)
        # for word in self.formatted_text.split(' '):
        #     if word:
        #         word = self.__spell_check(word)
        #         for product in products:
        #             if product == word:
        #                 # print('normal result: ', word)
        #                 result.append(word)
        return result

    def get_products(self,  directory, products):
        paths = []
        for root, _, files in os.walk("{}".format(directory)):
            for file in files:
                if file.endswith(".jpg"):
                    paths.append(os.path.join(root, file))
        for path in paths:
            # if not path == 'images/invoices/more/IMG_20180105_181004896.jpg':
            #     continue
            self.set_image(path)
            self.document_detection()
            self.format_doctext()
            result = self.find_products(products)
            print('{}: '.format(path), result)
            print()

    def get_products_image(self, path, products):
        self.set_image(path)
        self.document_detection()
        self.format_doctext()
        result = self.find_products(products)
        print('{}: '.format(path), result)
        print()

    def get_roi(self, region_data):
        print('getting roi ')
        print(self.text_props)
        for text in self.text_props.keys():
            text = self.__spell_check(text)
            # print(text)
            for element in region_data:
                if any(text == x for x in self.crop_hints):
                    # print(text)
                    self.y_min = self.text_props[text][0][1]
                if text == element:
                    # stores the TL y coordinate and BR y coordinates
                    # print('smmmm')
                    y = self.text_props[text][2][1]
                    if y > self.y_max:
                        self.y_max = y
        # sys.exit('done')
        print(self.y_max,self.y_min)
        return self.image[self.y_min - 5:self.y_max + 20, 0:]

    def __get_contents(self):
        print('getting contents')
        for text in self.all_text:
            for item in text.split(' '):
                if item and item != ' ':
                    c_item = self.__spell_check(item)
                    if c_item:
                        for obj in self.annotations:
                            o_item = self.__spell_check(obj.description)
                            if o_item:
                                if o_item == c_item:
                                    vertice = obj.bounding_poly.vertices
                                    self.contents[c_item] = [(vertice[0].x, vertice[0].y),
                                                             (vertice[1].x, vertice[1].y),
                                                             (vertice[2].x, vertice[2].y),
                                                             (vertice[3].x, vertice[3].y)]

        # print(self.contents)
        # sys.exit()

    # needs get_contents return val
    def get_rows(self):
        print('getting rows')
        # self.__get_contents()
        y_min = 0
        line = 1
        self.titles = []
        for key in self.text_props.keys():
            vertice = self.text_props[key]
            # print(vertice)
            if y_min == 0:
                y_min = (vertice[0][1] + vertice[3][1]) / 2
                self.rows['line{}'.format(line)] = []
            current_y = (vertice[0][1] + vertice[3][1]) / 2
            if (y_min - 10) <= current_y <= (y_min + 10):
                self.rows['line{}'.format(line)].append(key)
            else:
                y_min = current_y
                line = line + 1
                self.rows['line{}'.format(line)] = []
                self.rows['line{}'.format(line)].append(key)
        for row in self.rows.values():
            for element in row:
                if any(element == x for x in self.crop_hints):
                    self.titles = row
                    print('special row', row)
                    break
        print('rowwwwwwsss')
        print(self.rows)

    def get_columns(self):
        print('getting cols')
        # print(self.y_min, self.y_max)
        print(self.titles)
        for header in self.titles:
            props = self.text_props[header]
            x1, x2, y1 = props[0][0], props[1][0], props[2][1]
            x_mid = (x1 + x2) / 2
            self.cols[header] = []
            for key in self.text_props.keys():
                x_key = key
                if '(' in key:
                    x_key = key[0:key.index('(')]
                # print(key)
                props = self.text_props[x_key]
                x1, x2, y2 = props[0][0], props[1][0],props[2][1]
                if x1-20 < x_mid < x2+20 and y1 != y2:
                    self.cols[header].append(key)
        # for header in headers_list:
        #     times = 0
        #     x1, x2, y1 = self.contents[header][0][0], self.contents[header][1][0], self.contents[header][2][1]
        #     x_mid = (x1 + x2) / 2
        #     self.cols[header] = []
        #     for key in self.contents.keys():
        #         x1, x2, y2 = self.contents[key][0][0], self.contents[key][1][0], self.contents[key][2][1]
        #         if x1 < x_mid < x2 and y1 != y2:
        #             self.cols[header].append(key)
        print('columns')
        print(self.cols)
        # return self.cols

    def get_index(self):
        for x in self.crop_hints:
            for title in self.titles:
                if x == title:
                    self.index = x
                    break

    def map_contents(self):
        print('mapping contents')
        # self.get_rows()
        mapped = {}
        # print(self.all_text)
        # self.get_columns(self.titles)
        # sys.exit('done')
        print('all text')
        print(self.all_text)
        # sys.exit('done')
        for x in self.crop_hints:
            for title in self.titles:
                if x == title:
                    self.index = x
                    break
        print('index', self.index)
        for element in self.cols[self.index]:
            props = self.text_props[element]
            y1, y2 = props[0][1], props[3][1]
            y_mid = (y1 + y2) / 2
            mapped[element] = {}
            for title in self.titles:
                got = 0
                if title != self.index:
                    for col in self.cols[title]:
                        props = self.text_props[col]
                        y1, y2 = props[0][1], props[3][1]
                        if y1 < y_mid < y2:
                            mapped[element][title] = col
                            got = 1
                            break
                    if got == 0:
                        mapped[element][title] = None
        for key in mapped.keys():
            print(key)
            print(mapped[key])

    @staticmethod
    def to_digits(characters):
        final = ''
        for character in characters:
            if character.islower():
                character = character.upper()
            if character.isdigit():
                final = final + character
            elif character == 'B':
                final = final + '8'
            elif character == 'S':
                final = final + '5'
            elif character == 'O':
                final = final + '0'
            elif character == 'I':
                final = final + '1'
            elif character == 'Z':
                final = final + '2'
            else:
                final = final + character
        return final

    @staticmethod
    def to_alphabets(numbers):
        final = ''
        for number in numbers:
            if number.isalpha():
                final = final + number
            elif number == '1':
                final = final + 'I'
            elif number == '2':
                final = final + 'Z'
            elif number == '5':
                final = final + 'S'
            elif number == '8':
                final = final + 'B'
            elif number == '0':
                final = final + 'O'
            else:
                final = final + number
        return final


    @staticmethod
    def check_gst_format(word):
        if re.findall(r'\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d[Z]{1}[A-Z\d]{1}', word):
            return ''.join(re.findall(r'\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d[Z]{1}[A-Z\d]{1}', word))
        else:
            return None

    @staticmethod
    def probable_gst(word):
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

    def formatter(self, word):
        word = self.__cleaner(word)
        word = word.replace(' ', '')
        word = word.replace('.', '')
        word = word.replace('!', '')
        return word

    def change_gst_letters(self, subtext):
        final = ''
        try:
            subpart = subtext[0:2]
            if not subpart.isdigit():
                final = final + self.to_digits(subpart)
            else:
                final = final + subpart
            subpart = subtext[2:7]
            if not subpart.isalpha():
                final = final + self.to_alphabets(subpart)
            else:
                final = final + subpart
            subpart = subtext[7:11]
            if not subpart.isdigit():
                final = final + self.to_digits(subpart)
            else:
                final = final + subpart
            subpart = subtext[11]
            if not subpart.isalpha():
                final = final + self.to_alphabets(subpart)
            else:
                final = final + subpart
            subpart = subtext[12]
            if not subpart.isdigit():
                final = final + self.to_digits(subpart)
            else:
                final = final + subpart
            subpart = subtext[13]
            if subpart is not 'Z':
                final = final + 'Z'
            else:
                final = final + subpart
            final = final + subtext[14].upper()
            # print(final)
            return final
        except IndexError:
            # print('Exception Handled')
            return final

    def add_missing_gst(self, subtext=None):
        final = ''
        if subtext and 10 < len(subtext) < 15:
            # print(subtext)
            if self.gst_che(subtext):
                if re.findall(r'\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d[Z]{1}[A-Z\d]{1}', subtext):
                    return {subtext: True}
                return {subtext: 'probable'}
            else:
                return subtext
        print(subtext)
        subpart = subtext[0:2]
        if not subpart.isdigit():
            final = final + self.to_digits(subpart)
        else:
            final = final + subpart
        subpart = subtext[2:7]
        if not subpart.isalpha():
            final = final + self.to_alphabets(subpart)
        else:
            final = final + subpart
        subpart = subtext[7:11]
        if not subpart.isdigit():
            final = final + self.to_digits(subpart)
        else:
            final = final + subpart
        subpart = subtext[11]
        if not subpart.isalpha():
            final = final + self.to_alphabets(subpart)
        else:
            final = final + subpart
        subpart = subtext[12]
        if not subpart.isdigit():
            final = final + self.to_digits(subpart)
        else:
            final = final + subpart
        subpart = subtext[13]
        if subpart is not 'Z':
            final = final + 'Z'
        else:
            final = final + subpart
        final = final + subtext[14].upper()
        # print(final)
        return final

    def get_gst_inv_date(self, directory):
        paths = []
        for root, _, files in os.walk("{}".format(directory)):
            for file in files:
                if file.endswith(".jpg"):
                    paths.append(os.path.join(root, file))
        # print(paths)
        results = {}
        results["invoices"] = {}
        for path in paths:
            # if not path == 'images/invoices/batch3/IMG_20180115_120856634_HDR.jpg':
            #     continue
            # input('process {}?'.format(path))
            self.set_image(path)
            # print(path)
            # self.text_detection()
            self.document_detection()
            print(self.doc_all_text)
            result = results["invoices"][path] = {}
            dlno = result["DLNO"] = {}
            gstin = result["GSTIN"] = {}
            date = result["INV DATE"] = {}
            for text in self.doc_all_text:
                if self.probable_gst(text):
                    prob_gst = self.formatter(text)
                    if self.check_gst_format(prob_gst):
                        gstin[self.check_gst_format(prob_gst)] = True
                        continue
                    else:
                        prob_gst = ''.join(re.findall(r'[A-Z\d]{2}[A-Z]{5}\d{3,4}[A-Z\d]{3,4}', prob_gst))
                        prob_gst = self.change_gst_letters(prob_gst)
                        if self.check_gst_format(prob_gst):
                            gstin[self.check_gst_format(prob_gst)] = True
                            continue
                    # prob_gst = self.change_gst_letters(prob_gst)
                    prob_gst = ''.join(re.findall(r'[A-Z\d]{2}[A-Z]{5}\d{3,4}[A-Z\d]{3,4}', text))
                    if prob_gst:
                        prob_gst = self.change_gst_letters(prob_gst)
                        if self.check_gst_format(prob_gst):
                            gstin[prob_gst] = True
                        else:
                            gstin[prob_gst] = False

                if re.findall(r'\d+\/\d+A', text):
                    dlno[''.join(re.findall(r'\d+\/\d+A', text))] = True
                elif re.findall(r'\d+\/\d+\/\d+', text):
                    date[''.join(re.findall(r'\d+\/\d+\/\d+', text))] = True
        print(results)

    # def cropper_x(self, name):
    #     crop_img = self.image[:self.y_max, self]
    #     cv2.imwrite("{}.png".format(name), crop_img)

    # def __select_roi(self):
    #     for block in self.blocks:
    #         self.content[block.description] = [(block.bounding_poly.vertices[0].x, block.bounding_poly.vertices[0].y),
    #                                            (block.bounding_poly.vertices[2].x, block.bounding_poly.vertices[2].y)]
    #
    # def getMarkerPoints(self):
    #     '''
    #     detects and itereates the text found by api and stores the text and vertices in a dictionary
    #     for storing marking the ROI only
    #     '''
    #     # print('lol')
    #     for block in self.blocks:
    #         self.content[block.description] = [(block.bounding_poly.vertices[0].x, block.bounding_poly.vertices[0].y),
    #                                            (block.bounding_poly.vertices[2].x, block.bounding_poly.vertices[2].y)]
    #     if self.content is not None:
    #         return True, self.content
    #     return False, self.content
    #
    # def getCropperPoints(self):
    #     '''
    #     detects and itereates the text found by api and stores the text and vertices in a dictonary
    #     for cropping text
    #     '''
    #     for block in self.blocks:
    #         self.content[block.description] = [(block.bounding_poly.vertices[0].x, block.bounding_poly.vertices[0].y),
    #                                            (block.bounding_poly.vertices[
    #                                                 1].x, block.bounding_poly.vertices[1].y),
    #                                            (block.bounding_poly.vertices[
    #                                                 2].x, block.bounding_poly.vertices[2].y),
    #                                            (block.bounding_poly.vertices[3].x, block.bounding_poly.vertices[3].y)]
    #     return self.content
    #
