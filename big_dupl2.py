import pandas as pd
import re
from fuzzywuzzy import process, fuzz


class Big():
    def __init__(self):
        pass
    @staticmethod
    def name_matcher(self, name1, name2, total):
        n = []
        n.append(name2.upper())
        match = process.extract(name1.upper(), n, limit=3)[0][1]
        score = (match/100)*total
        return  score

    @staticmethod
    def checker(field1, field2,  score):
        if field1 == field2:
            score  = score + 15
            return True, score
        return False, score
    @classmethod
    def lol(self):
        bigdata = pd.read_excel(
            'MOCK_DATA.xlsx'
        )
        # writer = pd.ExcelWriter('extract90.xlsx')
        bigdata = bigdata.fillna('')
        bigdata['MatchSearchName'] = ''
        bigdata['match'] = ''
        print(bigdata.head(n=5))
        for pos1, obj1 in bigdata.iterrows():
            s = ''
            name1 = obj1['name']
            bigdata.set_value(pos1, 'MatchSearchName', name1)
            for pos2, obj2 in bigdata.iterrows():
                if pos1 != pos2:
                    name2 = obj2['name']
                    score = self.name_matcher(name1, name2, 40)
                    if 16 < score < 32:
                        if obj1['mobile'] == obj2['mobile']:
                            score = score + 20
                            _, score = self.checker(obj1['email'], obj2['email'], score=score)
                            _, score = self.checker(obj1['city'], obj2['city'], score=score)
                            _, score = self.checker(obj1['gender'], obj2['gender'], score=score)
                            _, score = self.checker(obj1['speciality'], obj2['speciality'], score=score)
                            print('16 to 32', name1, name2, score)
                            input('check')
                    elif score >= 32:
                        ch, score = self.checker(obj1['email'], obj2['email'], score=score)
                        if not ch:
                            score = self.name_matcher(name1, name2, score + 15)
                        ch, score = self.checker(obj1['city'], obj2['city'], score=score)
                        if not ch:
                            score = self.name_matcher(name1, name2, score + 15)
                        ch, score = self.checker(obj1['gender'], obj2['gender'], score=score)
                        if not ch:
                            score = self.name_matcher(name1, name2, score + 15)
                        ch, score = self.checker(obj1['speciality'], obj2['speciality'], score=score)
                        if not ch:
                            score = self.name_matcher(name1, name2, score + 15)
                        ch, score = self.checker(obj1['mobile'], obj2['mobile'], score=score)
                        if not ch:
                            score = self.name_matcher(name1, name2, score + 15)
                        print('>=32', name1, name2, score)
                        input('check')

    # bigdata.to_excel(writer, 'sheet1')
    # writer.save()
    # fl.close()
