from fuzzywuzzy import process, fuzz


class Big(object):
    @staticmethod
    def name_matcher(name1, name2, total):
        n = []
        n.append(name2.upper())
        match = process.extract(name1.upper(), n, limit=3)[0][1]
        print(match)
        score = (match/100)*total
        return score

    @staticmethod
    def checker(field1, field2,  score, ad):
        if field1 == field2 == '':
            return False, score
        if field1 == field2:
            score = score + ad
            return True, score
        return False, score

    @classmethod
    def field_checker(self, obj1, obj2, score, change):
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
        print('email', score, name)

        ch, score = self.checker(obj1['city'], obj2['city'], score=score, ad=10)
        if not ch:
            change = change + 10
            name = self.name_matcher(name1, name2, change)
        print('city', score, name)

        ch, score = self.checker(obj1['gender'], obj2['gender'], score=score, ad=5)
        if not ch:
            change = change + 5
            name = self.name_matcher(name1, name2, change)
        print('gender', score, name)

        ch, score = self.checker(obj1['speciality'], obj2['speciality'], score=score, ad=10)
        if not ch:
            change = change + 10
            name = self.name_matcher(name1, name2, change)
        print('spec', score, name)

        ch, score = self.checker(obj1['mobile'], obj2['mobile'], score=score, ad=15)
        print(change)
        if not ch:
            change = change + 15
            name = self.name_matcher(name1, name2, change)
        else:
            flag = flag + 1
        print('mobile', score, name)
        return score+name, flag

    @classmethod
    def lol(self, bigdata, writer):
        bigdata = bigdata.fillna('')
        for pos1, obj1 in bigdata.iterrows():
            s = ''
            name1 = obj1['name']
            bigdata.set_value(pos1, 'MatchSearchName', name1)
            for pos2, obj2 in bigdata.iterrows():
                if pos1 != pos2:
                    name2 = obj2['name']
                    print(name1, name2)
                    name = self.name_matcher(name1, name2, 40)
                    print('on 40', name)
                    # input('check')
                    if 16 < name < 32:
                        if obj1['mobile'] == obj2['mobile'] or obj2['email'] == obj1['email']:
                            score, flag = self.field_checker(obj1=obj1, obj2=obj2, score=name, change=40)
                            print('16 to 32', name1, name2, score)
                            if score >= 90 or flag > 0:
                                s = name1 + ' ' + name2 + ' ' + obj1['email'] + ' ' + obj2['email'] + ' ' + obj1['city']\
                                    + ' ' + obj2['city'] + ' ' + str(obj1['mobile']) + ' ' + str(obj2['mobile']) + ' ' + \
                                    obj1['speciality'] + ' ' + obj2['speciality'] + ' ' + obj1['gender'] + ' ' + \
                                    obj2['gender'] + str(score) + ' '
                                bigdata.set_value(pos1, 'match', s)
                            # input('check')
                    elif name >= 32:
                        score, flag = self.field_checker(obj1=obj1, obj2=obj2, score=name, change=40)
                        print('>=32', name1, name2, score)
                        if score >= 90 or flag > 0:
                            s = name1 + ' ' + name2 + ' ' + obj1['email'] + ' ' + obj2['email'] + ' ' + obj1['city'] \
                                + ' ' + obj2['city'] + ' ' + str(obj1['mobile']) + ' ' + str(obj2['mobile']) + ' ' + \
                                obj1['speciality'] + ' ' + obj2['speciality'] + ' ' + obj1['gender'] + ' ' + \
                                obj2['gender'] + str(score) + ' '
                            bigdata.set_value(pos1, 'match', s)
                        # input('check')
        return bigdata, writer

