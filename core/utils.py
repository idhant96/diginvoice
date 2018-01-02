import re
import cv2
import json


def resize(image):
    r = 400.0 / image.shape[1]
    dim = (300, int(image.shape[0] * r))
    # perform the actual resizing of the image and show it
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized

def cleaner(st):
    # print('text cleaning')
    st = st.encode('ascii', 'ignore').decode('utf-8')
    return re.sub(r'[(?|$|,+''"”*#.:|!)]', r'', st)

def get_data(file_name, obj):
    with open('data/{}.json'.format(file_name)) as fh:
        data = json.load(fh)
    return data['{}'.format(obj)]