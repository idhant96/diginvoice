import io
import json
from enchant import DictWithPWL
from enchant.checker import SpellChecker
import enchant
import cv2
from google.cloud import vision
from google.cloud.vision import types
import re
import sys

'''
to Jay Sir
Functions needs to be distributed
uncomment the prints to come out of debugging mode
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
        self.crop_hints = ['PRODUCTS','Particulars','PARTICULARS', 'PRODUCT']
        self.index = None
        self.o_item = []
        self.image = None
        self.dictionary = None
        self.personal = None
        self.checker = None
        self.rows = {}
        self.cols = {}
        self.all_text = ''
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
        # self.image =  cv2.adaptiveThreshold(self.image,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        #     cv2.THRESH_BINARY,21,7)
        # self.image = self.__resize(self.image)

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
        # print(self.all_text)

    def get_props(self):
        self.text_props = {}
        times = 1
        print(self.all_text)
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
            if (y_min - 40) <= current_y <= (y_min + 40):
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
                if x1-40 < x_mid < x2+40 and y1 != y2:
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
    def marker(self, roi):
        '''''
        marks the regions of interest
        '''
        # print('lol2')
        for key in self.content.keys():
            if key in roi:
                TL, BR = self.content[key]
                cv2.rectangle(self.image, TL, BR, (0, 255, 0), 1)
        return self.image
