from fuzzywuzzy import process
cimport numpy as np

class Big(object):

    cdef np.ndarray


    @staticmethod
    def name_matcher(str name1, str name2, int total):
        n = []
        n.append(name2.upper())
        match = process.extract(name1.upper(), n, limit=3)[0][1]
        cdef double score = (match/100)*total
        return score

    @staticmethod
    def checker(str field1, str field2, double score, int ad):
        if field1 == field2 == NULL:
            return False, score
        if field1 == field2:
            score = score + ad
            return True, score
        return False, score

    @classmethod
    def field_checker(self,object obj1,object obj2, double score, int change):
        name1 = obj1['name']
        name2 = obj2['name']
        # print(obj1)
        cdef double name = score
        score = 0
        cdef short flag = 0
        # print(name1)
        ch, score = self.checker(obj1.email, obj2.email, score=score, ad=20)
        if not ch:
            change = change + 20
            name = self.name_matcher(name1, name2, change)
        else:
            flag = flag + 1
        # print(self.checker(obj1['city'], obj2['city'], score=score, ad=10))
        ch, score = self.checker(obj1.city, obj2.city, score=score, ad=10)
        if not ch:
            change = change + 10
            name = self.name_matcher(name1, name2, change)
        ch, score = self.checker(obj1.gender, obj2.gender, score=score, ad=5)
        if not ch:
            change = change + 5
            name = self.name_matcher(name1, name2, change)
        ch, score = self.checker(obj1.speciality, obj2.speciality, score=score, ad=10)
        if not ch:
            change = change + 10
            name = self.name_matcher(name1, name2, change)
        ch, score = self.checker(obj1.mobile, obj2.mobile, score=score, ad=15)
        if not ch:
            change = change + 15
            name = self.name_matcher(name1, name2, change)
        else:
            flag = flag + 1
        return score+name, flag

    @classmethod
    def dup(self, bigdata):
        cdef double name
        cdef short flag = 0
        cdef double score
        for pos1, obj1 in bigdata.iterrows():
            s = ''
            name1 = obj1['name']
            bigdata.set_value(pos1, 'MatchSearchName', name1)
            for pos2, obj2 in bigdata.iterrows():
                if pos1 < pos2:
                    name2 = obj2['name']
                    # print(name1)
                    name = self.name_matcher(name1, name2, 40)
                    if 16 < name < 32:
                        if obj1.mobile == obj2.mobile or obj2.email == obj1.email:
                            score, flag = self.field_checker(obj1, obj2, name, 40)
                            if score >= 80 or flag > 0:
                                s = name1 + ' ' + name2 + ' ' + obj1.email + ' ' + obj2.email + ' ' + obj1['city'] \
                                + ' ' + obj2['city'] + ' ' + str(obj1['mobile']) + ' ' + str(obj2['mobile']) + ' ' + \
                                obj1['speciality'] + ' ' + obj2['speciality'] + ' ' + obj1['gender'] + ' ' + \
                                obj2['gender'] + str(score) + ' '
                                bigdata.set_value(pos1, 'match', s)
                    elif name >= 32:
                        score, flag = self.field_checker(obj1, obj2, name, 40)
                        if score >= 90 or flag > 0:
                            s = name1 + ' ' + name2 + ' ' + obj1.email + ' ' + obj2.email + ' ' + obj1['city'] \
                                + ' ' + obj2['city'] + ' ' + str(obj1['mobile']) + ' ' + str(obj2['mobile']) + ' ' + \
                                obj1['speciality'] + ' ' + obj2['speciality'] + ' ' + obj1['gender'] + ' ' + \
                                obj2['gender'] + str(score) + ' '
                            bigdata.set_value(pos1, 'match', s)
        return bigdata