# import hunspell
import io

import cv2
import numpy as np
from google.cloud import vision
from google.cloud.vision import types

# spellchecker = hunspell.HunSpell('/Library/Spelling/en_US.dic',
#                                  '/Library/Spelling/en_US.aff')

"""Detects document features in an image."""

#
# def correct_words(spellchecker, words, add_to_dict=[]):
#     """
#     get the correct spelling for the work in the text
#     """
#     # get the encoding for later use in decode()
#     enc = spellchecker.get_dic_encoding()
#
#     # add custom words to the dictionary
#     for w in add_to_dict:
#         spellchecker.add(w)
#
#     # auto-correct words
#     corrected = []
#     for w in words:
#         ok = spellchecker.spell(w)  # check spelling
#         if not ok:
#             suggestions = spellchecker.suggest(w)
#             if len(suggestions) > 0:  # there are suggestions
#                 best = suggestions[0].decode(enc)  # best suggestions (decoded to str)
#                 corrected.append(best)
#             else:
#                 corrected.append(w)  # there's no suggestion for a correct word
#         else:
#             corrected.append(w)  # this word is correct
#
#     return corrected


# get google vision client
client = vision.ImageAnnotatorClient()

# open image file to extract text
with io.open('images/vision.jpeg', 'rb') as image_file:
    content = image_file.read()

# prepare image
image = types.Image(content=content)

# detect text
response = client.document_text_detection(image=image)

# get full document
document = response.full_text_annotation

# prepare array of all words
symbols = []
paragraphs = []
for page in document.pages:
    for block in page.blocks:
        for paragraph in block.paragraphs:
            para = ""
            for word in paragraph.words:
                text = ""
                for symbol in word.symbols:
                    if symbol.text != '.':
                        text += symbol.text

                symbols.append(
                    {"text": correct_words(spellchecker, [text], ["GSTIN"])[0],
                     "coordinates": [word.bounding_box.vertices[0], word.bounding_box.vertices[2]]})
                para += correct_words(spellchecker, [text], ["GSTIN"])[0] + ' '
            paragraphs.append(para)
            print para

# get dimensions of image
image1 = cv2.imread('invoice1.jpg')
height, width, channels = image1.shape

# Create a black image
img = np.zeros((height, width, 3), np.uint8)
img.fill(255)