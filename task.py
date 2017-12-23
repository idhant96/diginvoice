import io
from google.cloud import vision
from google.cloud.vision import types
import json
import operator
from enchant import DictWithPWL
from enchant.checker import SpellChecker
import enchant
import re
'''
QTY is not spell checkable

'''
# stores words with coordinates
contents = {}
#stores spell checked words
check = []
#stores the data in form of rows
rows = {}
cols = {}

#  Headers Data
data = None
with open('data/headers.json') as fh:
    data = json.load(fh)
# with open('data/products.json') as fh:
#     data2 = json.load(fh)

# Init the enchant dictionaries
dictionary = DictWithPWL("en_US")
a = enchant.Dict()

#Adding the personal words to dict
for element in data['table']:
    a.add(element)



# init the google client
google_vision_client = vision.ImageAnnotatorClient()
with io.open('images/first.jpg', 'rb') as image_file:
    data = image_file.read()
vision_image = types.Image(content=data)

# detect text
response = google_vision_client.text_detection(image=vision_image)
annotations = response.text_annotations
all_text = annotations[0].description.split('\n')

def reg_cleaner(strs):
    return re.sub(r'[(?|$|,+"”.:|!)]',r' ',strs)

# Note the image needs to be processed for proper dimensions
def get_contents():
    for text in all_text:
        # cleaned = reg_cleaner(text)
        for item in text.split(' '):
            if item and item != ' ':
                for object in annotations:
                    if object.description == item:
                        vertice = object.bounding_poly.vertices
                        contents[item] = [(vertice[0].x,vertice[0].y),
                                          (vertice[1].x,vertice[1].y),
                                          (vertice[2].x,vertice[2].y),
                                          (vertice[3].x,vertice[3].y)]


#needs get_contents return val
def get_rows(content_data):
    y_min = 0
    line = 1
    for key in content_data.keys():
        vertice = content_data[key]
        if y_min == 0:
            y_min = (vertice[0][1] + vertice[3][1]) / 2
            rows['line{}'.format(line)] = []
        current_y = (vertice[0][1] + vertice[3][1]) / 2
        if (y_min - 10) <= current_y <= (y_min + 10):
            rows['line{}'.format(line)].append(key)
        else:
            y_min = current_y
            line = line + 1
            rows['line{}'.format(line)] = []
            rows['line{}'.format(line)].append(key)



def get_column(headers_list):
    for header in headers_list:
        x1,x2 = contents[header][0][0],contents[header][1][0]
        x_mid = (x1+x2) / 2
        cols[header] = []
        for key in contents.keys():
            x1,x2 = contents[key][0][0],contents[key][1][0]
            if x1 < x_mid < x2:
                cols[header].append(key)





get_contents()
get_rows(contents)
headers = rows['line14']
get_column(headers)
for col in cols:
    print('{}: '.format(col),cols[col])
    print('')








# Checking the words to be in headers
def spell_check(e_words):
    if e_words:
        checker = SpellChecker(dictionary)
        checker.set_text(e_words)
        if checker.check(e_words) is False:
            if a.check(e_words) is False:
                if a.suggest(e_words) != []:
                    for x in data['table']:
                        if x == a.suggest(e_words)[0]:
                            # print('corrected by a: ', e_words)
                            check.append(x)
                            break
                # print('no suggestions', e_words)
            else:
                # print('was in a', e_words)
                check.append(e_words)
        else:
            for x in data['table']:
                if x == e_words:
                    # print('corrected by a: ', e_words)
                    check.append(x)
                    break

# for elements in words:
#     for word in elements.split(' '):
#         if word:
#             spell_check(word)
#
# for values in p:
#     for value in values.split(' '):
#         for object in content:
#             if value == object.description:
#                 contents[value] = object.bounding_poly.vertices[0].x
# sorted_x = sorted(contents.items(), key=operator.itemgetter(1))
#
# for element,_ in sorted_x:
#     for object in content:
#         if element == object.description:
#             contents[element] = object.bounding_poly.vertices