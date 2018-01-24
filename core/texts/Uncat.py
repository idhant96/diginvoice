import cv2


def get_roi(self, region_data):
    print('getting roi ')
    print(self.text_props)
    for text in self.text_props.keys():
        text = self.__spell_check(text)
        # print(texts)
        for element in region_data:
            if any(text == x for x in self.crop_hints):
                # print(texts)
                self.y_min = self.text_props[text][0][1]
            if text == element:
                # stores the TL y coordinate and BR y coordinates
                # print('smmmm')
                y = self.text_props[text][2][1]
                if y > self.y_max:
                    self.y_max = y
    # sys.exit('done')
    print(self.y_max, self.y_min)
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
        if (y_min - 10) <= current_y <= (y_min + 10):
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
            x1, x2, y2 = props[0][0], props[1][0], props[2][1]
            if x1 - 20 < x_mid < x2 + 20 and y1 != y2:
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
    print('all texts')
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

def cropper_x(self, name):
    crop_img = self.image[:self.y_max, self]
    cv2.imwrite("{}.png".format(name), crop_img)

def __select_roi(self):
    for block in self.blocks:
        self.content[block.description] = [(block.bounding_poly.vertices[0].x, block.bounding_poly.vertices[0].y),
                                           (block.bounding_poly.vertices[2].x, block.bounding_poly.vertices[2].y)]

def getMarkerPoints(self):
    '''
    detects and itereates the texts found by api and stores the texts and vertices in a dictionary
    for storing marking the ROI only
    '''
    # print('lol')
    for block in self.blocks:
        self.content[block.description] = [(block.bounding_poly.vertices[0].x, block.bounding_poly.vertices[0].y),
                                           (block.bounding_poly.vertices[2].x, block.bounding_poly.vertices[2].y)]
    if self.content is not None:
        return True, self.content
    return False, self.content

def getCropperPoints(self):
    '''
    detects and itereates the texts found by api and stores the texts and vertices in a dictonary
    for cropping texts
    '''
    for block in self.blocks:
        self.content[block.description] = [(block.bounding_poly.vertices[0].x, block.bounding_poly.vertices[0].y),
                                           (block.bounding_poly.vertices[
                                                1].x, block.bounding_poly.vertices[1].y),
                                           (block.bounding_poly.vertices[
                                                2].x, block.bounding_poly.vertices[2].y),
                                           (block.bounding_poly.vertices[3].x, block.bounding_poly.vertices[3].y)]
    return self.content