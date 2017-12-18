import numpy as np
import io
import cv2
from google.cloud import vision
from google.cloud.vision import types
import sys


class Ocr:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        self.image = self.prep_image = None
        self.content = {}
        self.y_val = self.x_val = {}
        self.y_min = self.y_max = self.x_min = self.x_max = 0
        self.executed = False
        self.blocks = self.document = self.doc_blocks = None

    def prepare_image(self, img):
        self.image = cv2.imread('{}'.format(img))
        with io.open("{}".format(img), 'rb') as image_file:
            data = image_file.read()
        self.prep_image = types.Image(content=data)
        self.executed = True

    def compute_contents(self, mode=1):
        '''
        :param type:
        :return:
        '''
        if self.executed is not True:
            sys.exit('The API request was not prepared')
        if mode == 1:
            response = self.client.text_detection(image=self.prep_image)
            self.blocks = response.text_annotations
        elif mode == 2:
            response = self.client.document_text_detection(image=self.prep_image)
            self.document = response.full_text_annotation
        else:
            sys.exit('Invalid Type request')

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

    def search_col(self, title):
        x1 = x2 = 0
        for block in self.blocks:
            if block.description == title:
                (x1,x2) = (block.bounding_poly.vertices[3].x,block.bounding_poly.vertices[2].x)
                break
        crop_img = self.image[self.y_min[0]:self.y_max[1],x1:x2]
        cv2.imwrite('{}.png'.format(title), crop_img)

    def __search_y(self, any_list):
        # stores the y values (min and max ) for any given data (list)
        for block in self.blocks:
            if block.description in any_list:
                # stores the TL y coordinate and BR u cordinate
                self.y_val[block.description] = (block.bounding_poly.vertices[0].y, block.bounding_poly.vertices[2].y)
        self.y_min = min(self.y_val.values(), key=lambda t: t[0])
        self.y_max = max(self.y_val.values(), key=lambda t: t[1])
        #
        # self.y_min = min(list(self.y_val.values()))
        # self.y_max = max(list(self.y_val.values()))

    def __search_x(self, any_list):
        for block in self.blocks:
            if block.description in any_list:
                #storing TL x cordinate  and
                self.x_val[block.description] = (block.bounding_poly.vertices[0].x,block.bounding_poly.vertices[1].x)
        # self.x_min = min(list(self.x_val.values()))
        # self.x_max = max(list(self.x_val.values()))
        self.x_min = min(self.x_val.values(), key=lambda t: t[0])
        self.x_max = max(self.x_val.values(), key=lambda t: t[1])

    def select_roi_y(self, any_list_y):
        self.__search_y(any_list_y)

    def select_roi_x(self, any_list_x):
        self.__search_x(any_list_x)

    def cropper_y(self, name):
        crop_img = self.image[self.y_min[0]:self.y_max[1], 0:]
        cv2.imwrite("{}.png".format(name), crop_img)
        #return crop_img

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
