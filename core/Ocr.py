import io
import json
from enchant import DictWithPWL
from enchant.checker import SpellChecker
import enchant
import cv2
from google.cloud import vision
from google.cloud.vision import types
import re

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
        self.content = {}
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

        # format image into google vision understandable
        with io.open(self.image_path, 'rb') as image_file:
            data = image_file.read()
        vision_image = types.Image(content=data)

        # detect text
        response = Ocr.google_vision_client.text_detection(image=vision_image)

        # get all detected blocks
        return response.text_annotations

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

    def get_roi(self, annotations,dict_data,region_data):
        for obj in annotations:
            word = self.__spell_check(obj.description, dict_data)
            if word is None:
                continue
            for element in region_data:
                if word == element:
                    # stores the TL y coordinate and BR y coordinat
                    vertice = obj.bounding_poly.vertices
                    # remove the dict for production code
                    self.y_val[obj.description] = (vertice[0].y, vertice[2].y)
        # remove static variables for production code
        self.y_min = min(self.y_val.values(), key=lambda t: t[0])
        self.y_max = max(self.y_val.values(), key=lambda t: t[1])
        return self.image[self.y_min[0]:self.y_max[1], 0:]

    def search_col(self, title):
        x1 = x2 = 0
        for block in self.blocks:
            if block.description == title:
                (x1, x2) = (block.bounding_poly.vertices[3].x, block.bounding_poly.vertices[2].x)
                break
        crop_img = self.image[self.y_min[0]:self.y_max[1], x1:x2]
        cv2.imwrite('{}.png'.format(title), crop_img)

    def __search_y(self, any_list):
        # stores the y values (min and max ) for any given data (list)
        for block in self.blocks:
            if block.description in any_list:
                # stores the TL y coordinate and BR y coordinat
                vertice = block.bounding_poly.vertices
                self.y_val[block.description] = (vertice[0].y, vertice[2].y)
        self.y_min = min(self.y_val.values(), key=lambda t: t[0])
        self.y_max = max(self.y_val.values(), key=lambda t: t[1])
        #
        # self.y_min = min(list(self.y_val.values()))
        # self.y_max = max(list(self.y_val.values()))

    def cropper_y(self, name):
        crop_img = self.image[self.y_min[0]:self.y_max[1], 0:]
        cv2.imwrite("{}.png".format(name), crop_img)
        # return crop_img

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
