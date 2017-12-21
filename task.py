import io
from google.cloud import vision
from google.cloud.vision import types
import json
import operator
from enchant import DictWithPWL
from enchant.checker import SpellChecker
import enchant

data = None
with open('data/headers.json') as fh:
    data = json.load(fh)
dictionary = DictWithPWL("en_US")
checker = SpellChecker(dictionary)
a = enchant.Dict()
for element in data['table']:
    a.add(element)

def spell_check(e_words):
    if a.check(e_words) is not True:
        if a.suggest(e_words) is not None:
            # print("no",a.suggest(e_words)[0])
            try:
                return a.suggest(e_words)[0]
            except IndexError:
                return e_words
        else:
            print("here",e_words)
            return e_words
    return e_words




google_vision_client = vision.ImageAnnotatorClient()
with io.open('images/first.jpg', 'rb') as image_file:
    data = image_file.read()
vision_image = types.Image(content=data)
p = []
contents = {}
# detect text
response = google_vision_client.text_detection(image=vision_image)
content = response.text_annotations
words = content[0].description.split('\n')
# words = words.translate(None, '!@#$",')
checked = ' '
with open('data/headers.json') as fh:
    data = json.load(fh)
for elements in words:
    for element in elements.split(' '):
        checked = checked + spell_check(element) + ' '
        #     checked = spell_check(element)
        #     #print(element)
        #     if values == checked:
        #         if checked not in p:
        #             p.append(elements)


print(checked)
for values in p:
    for value in values.split(' '):
        for object in content:
            if value == object.description:
                contents[value] = object.bounding_poly.vertices[0].x
sorted_x = sorted(contents.items(), key=operator.itemgetter(1))

for element,_ in sorted_x:
    for object in content:
        if element == object.description:
            contents[element] = object.bounding_poly.vertices
#
# # print(spell_check(p))
# print(p)
# # print(words)
# # print(contents)



