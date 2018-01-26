from google.cloud import vision
from google.cloud.vision import types
import io


class Ocr(object):
    google_vision_client = vision.ImageAnnotatorClient()
    image_path = ''
    image = None
    data = None

    @staticmethod
    def get_data(path):
        with io.open(path, 'rb') as image_file:
            data = image_file.read()
        return data

    @classmethod
    def document_detection(cls, img):
        cls.image_path = '{}'.format(img)
        data = cls.get_data(cls.image_path)
        vision_image = types.Image(content=data)
        response = cls.google_vision_client.document_text_detection(image=vision_image)
        annotations = response.text_annotations
        doc_all_text = annotations[0].description.split('\n')
        return annotations, doc_all_text

    @classmethod
    def text_detection(cls, img):
        cls.image_path = '{}'.format(img)
        data = cls.get_data(cls.image_path)
        vision_image = types.Image(content=data)
        response = Ocr.google_vision_client.text_detection(image=vision_image)
        annotations = response.text_annotations
        all_text = annotations[0].description.split('\n')
        return annotations, all_text
