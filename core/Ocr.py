import io
import json
from enchant import DictWithPWL
from enchant.checker import SpellChecker
import enchant
import cv2
from google.cloud import vision
from google.cloud.vision import types
import re
import numpy as np

'''
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
        self.image = None
        self.dictionary = None
        self.personal = None
        self.checker = None
        self.rows = self.cols = {}
        self.all_text = ''
        self.contents = {}
        self.roi = []
        self.titles = []
        self.response = self.annotations = None
        self.y_val = self.x_val = {}
        self.y_min = self.y_max = self.x_min = self.x_max = 0
        self.blocks = self.document = self.doc_blocks = None

    def __cleaner(self,strs):
        return re.sub(r'[(?|$|,+''"”*#.:|!)]', r'', strs)

    def load_spellings(self,data):
        self.dictionary = DictWithPWL("en_US")
        self.checker = SpellChecker(self.dictionary)
        self.personal = enchant.Dict()
        # Adding the personal words to dict
        for element in data:
            self.personal.add(element)

    def __spell_check(self, e_word, data):
        e_word = self.__cleaner(e_word)
        if e_word:
            self.checker.set_text(e_word)
            if self.checker.check(e_word) is False:
                if self.personal.check(e_word) is False:
                    if self.personal.suggest(e_word) != []:
                        for element in data:
                            if element == self.personal.suggest(e_word)[0]:
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
        self.image = cv2.imread(self.image_path)

    def text_detection(self):
        """
        detect text from the image
        :return:
        """
        print(self.image_path)
        # format image into google vision understandable
        with io.open(self.image_path, 'rb') as image_file:
            data = image_file.read()
        vision_image = types.Image(content=data)

        # detect text
        self.response = Ocr.google_vision_client.text_detection(image=vision_image)
        self.annotations = self.response.text_annotations
        self.all_text = self.annotations[0].description.split('\n')
        #print(self.all_text)
        print('getting')


    def get_data(self, file_name, obj):
        with open('data/{}.json'.format(file_name)) as fh:
            data = json.load(fh)
        return data['{}'.format(obj)]

    def document_text_detection(self):
        """
        detect document from image
        :return:
        """
        # format image into google vision understandable
        with io.open(self.image_path, 'rb') as image_file:
            data = image_file.read()
        vision_image = types.Image(content=data)

        # detect text
        response = Ocr.google_vision_client.document_text_detection(image=vision_image)

        # get all detected blocks
        return response.full_text_annotation

    def compute_document(self):
        '''
        Computes the document ocr of vision api
        :return:
        '''
        for page in self.document.pages:
            for self.doc_blocks in page.blocks:
                block_words = []
                for paragraph in self.doc_blocks.paragraphs:
                    block_words.extend(paragraph.words)
                block_symbols = []
                for word in block_words:
                    block_symbols.extend(word.symbols)

                block_text = ''
                for symbol in block_symbols:
                    block_text = block_text + symbol.text

                print('Block Content: {}'.format(block_text))
                print('Block Bounds:\n {}'.format(self.doc_blocks.bounding_box))

    def get_roi(self,dict_data,region_data):
        for obj in self.annotations:
            word = self.__spell_check(obj.description, dict_data)
            if word is None:
                continue
            for element in region_data:
                if word == 'PARTICULARS':
                    self.y_min = obj.bounding_poly.vertices[0].y

                if word == element:
                    # stores the TL y coordinate and BR y coordinat
                    y = obj.bounding_poly.vertices[2].y
                    if y > self.y_max:
                        self.y_max = y

                    # remove the dict for production code
                    # self.y_val[obj.description] = (vertice[0].y, vertice[2].y)
        # remove static variables for production code
        # self.y_min = min(self.y_val.values(), key=lambda t: t[0])
        #
        # self.y_max = max(self.y_val.values(), key=lambda t: t[1])
        #self.roi = self.image[self.y_min[0]:self.y_max[1], 0:]
        return self.image[self.y_min-5:self.y_max+20, 0:]

    def search_col(self, title):
        x1 = x2 = 0
        for block in self.blocks:
            if block.description == title:
                (x1, x2) = (block.bounding_poly.vertices[3].x, block.bounding_poly.vertices[2].x)
                break
        crop_img = self.image[self.y_min[0]:self.y_max[1], x1:x2]
        cv2.imwrite('{}.png'.format(title), crop_img)

    def __get_contents(self):
        print('lol')
        for text in self.all_text:
            # cleaned = reg_cleaner(text)
            for item in text.split(' '):
                if item and item != ' ':
                    for object in self.annotations:
                        if object.description == item:
                            vertice = object.bounding_poly.vertices
                            self.contents[item] = [(vertice[0].x, vertice[0].y),
                                              (vertice[1].x, vertice[1].y),
                                              (vertice[2].x, vertice[2].y),
                                              (vertice[3].x, vertice[3].y)]

    # needs get_contents return val
    def get_rows(self):
        self.__get_contents()
        y_min = 0
        line = 1
        self.titles = []
        for key in self.contents.keys():
            vertice = self.contents[key]
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
                if 'PARTICULARS' in element:
                    self.titles = row
                    print(row)
                    break

        return self.rows

    def get_columns(self,headers_list):
        for header in headers_list:
            x1, x2 = self.contents[header][0][0], self.contents[header][1][0]
            x_mid = (x1 + x2) / 2
            self.cols[header] = []
            for key in self.contents.keys():
                x1, x2 , y1, y2= self.contents[key][0][0], self.contents[key][1][0],self.contents[key][0][1], self.contents[key][2][1]

                if x1 < x_mid < x2 and y1 >= self.y_min and y2 <= self.y_max :
                    self.cols[header].append(key)


    def map_contents(self):
        self.get_rows()
        titles = []
        mapped = []
        self.get_columns(self.titles)
        for row in self.rows.values():
            for row_element in row:
                r = []
                for col in self.cols.values():
                    for col_element in col:
                        if row_element == col_element:
                            r.append(row_element)
            mapped.append(r)
        # print(self.rows)
        print(self.cols)
        # print(mapped)










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
