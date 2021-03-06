from fuzzywuzzy import process
# import time


class Big(object):
    @staticmethod
    def name_matcher(name1, name2, total):
        # startTime = time.time() * 1000
        n = []
        n.append(name2.upper())
        match = process.extract(name1.upper(), n, limit=3)[0][1]
        score = (match/100)*total
        # print('name_matcher ', time.time() * 1000 - startTime)
        return score

    @staticmethod
    def checker(field1, field2,  score, ad):
        # startTime = time.time() * 1000
        if field1 == field2 == '':
            return False, score
        if field1 == field2:
            score = score + ad
            # print('checker ', time.time() * 1000- startTime)
            return True, score
        # print('checker ', time.time() * 1000 - startTime)
        return False, score

    @classmethod
    def field_checker(self, obj1, obj2, score, change):
        # startTime = time.time() * 1000
        name1 = obj1['name']
        name2 = obj2['name']
        name = score
        score = 0
        flag = 0
        ch, score = self.checker(obj1['email'], obj2['email'], score=score, ad=20)
        if not ch:
            change = change + 20
            name = self.name_matcher(name1, name2, change)
        else:
            flag = flag + 1
        ch, score = self.checker(obj1['city'], obj2['city'], score=score, ad=10)
        if not ch:
            change = change + 10
            name = self.name_matcher(name1, name2, change)
        ch, score = self.checker(obj1['gender'], obj2['gender'], score=score, ad=5)
        if not ch:
            change = change + 5
            name = self.name_matcher(name1, name2, change)
        ch, score = self.checker(obj1['speciality'], obj2['speciality'], score=score, ad=10)
        if not ch:
            change = change + 10
            name = self.name_matcher(name1, name2, change)
        ch, score = self.checker(obj1['mobile'], obj2['mobile'], score=score, ad=15)
        if not ch:
            change = change + 15
            name = self.name_matcher(name1, name2, change)
        else:
            flag = flag + 1
        # print('field_checkr ', time.time() * 1000 - startTime)
        return score+name, flag

    @classmethod
    def dup(self, bigdata):
        # print('started')
        # startTime = time.time() * 1000
        for pos1, obj1 in bigdata.iterrows():
            s = ''
            name1 = obj1['name']
            bigdata.set_value(pos1, 'MatchSearchName', name1)
            for pos2, obj2 in bigdata.iterrows():
                # print('reached')
                if pos1 < pos2:
                    name2 = obj2['name']
                    # print(name1)
                    name = self.name_matcher(name1, name2, 40)
                    # print('on 40', name)
                    # input('check')
                    if 16 < name < 32:
                        if obj1['mobile'] == obj2['mobile'] or obj2['email'] == obj1['email']:
                            score, flag = self.field_checker(obj1=obj1, obj2=obj2, score=name, change=40)
                            if score >= 90 or flag > 0:
                                s = s + name1 + ' ' + name2 + ' ' + obj1['email'] + ' ' + obj2['email'] + ' ' + obj1['city']\
                                    + ' ' + obj2['city'] + ' ' + str(obj1['mobile']) + ' ' + str(obj2['mobile']) + ' ' + \
                                    obj1['speciality'] + ' ' + obj2['speciality'] + ' ' + obj1['gender'] + ' ' + \
                                    obj2['gender'] + str(score) + ' '
                                bigdata.set_value(pos1, 'match', s)
                            # input('check')
                    elif name >= 32:
                        score, flag = self.field_checker(obj1=obj1, obj2=obj2, score=name, change=40)
                        # print('>=32', name1, name2, score)
                        if score >= 90 or flag > 0:
                            s = s + name1 + ' ' + name2 + ' ' + obj1['email'] + ' ' + obj2['email'] + ' ' + obj1['city'] \
                                + ' ' + obj2['city'] + ' ' + str(obj1['mobile']) + ' ' + str(obj2['mobile']) + ' ' + \
                                obj1['speciality'] + ' ' + obj2['speciality'] + ' ' + obj1['gender'] + ' ' + \
                                obj2['gender'] + str(score) + ' '
                            bigdata.set_value(pos1, 'match', s)
                            # result = (pos1, s)
                        # input('check')
        # print('dup ', time.time() * 1000 - startTime)
        return bigdata


