from google.cloud import vision
from google.cloud.vision import types
import cv2
import io


google_vision_client = vision.ImageAnnotatorClient()
image = cv2.imread('{}'.format('invoices/invoice1.jpg'))
with io.open("{}".format('invoices/invoice1.jpg'), 'rb') as image_file:
    data = image_file.read()
prep_image = types.Image(content=data)


response = google_vision_client.text_detection(image=prep_image)
texts = response.text_annotations

for text in texts:
    print(text.description)
    # print('\n"{}"'.format(text.description))

    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in text.bounding_poly.vertices])

    print('bounds: {}'.format(','.join(vertices)))