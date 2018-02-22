from fuzzywuzzy import process
import multiprocessing
import pandas as pd


class Big(object):
    @classmethod
    def get_pos(self, file_path):
        df = pd.read_excel(file_path)
        df = df.fillna('')
        num_processes = multiprocessing.cpu_count() - 1
        chunk_size = int(df.shape[0] / num_processes)
        chunks = [df.ix[df.index[i:i + chunk_size]] for i in range(0, df.shape[0], chunk_size)]
        pool = multiprocessing.Pool(processes=num_processes)
        objects = []
        for i in range(len(chunks)):
            for j in range(len(chunks)):
                if i < j:
                    objects.append((chunks[i], chunks[j]))
        return pool.starmap(self.dup, objects)

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
        ch, score = self.checker(obj1['email'], obj2['email'], score=score, ad=20)
        if not ch:
            change = change + 20
            name = self.name_matcher(name1, name2, change)
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
        # print('field_checkr ', time.time() * 1000 - startTime)
        return score+name

    @classmethod
    def dup(self, chunk1, chunk2):
        p = {}
        # print('started')
        # startTime = time.time() * 1000
        for pos1, obj1 in chunk1.iterrows():
            s = []
            name1 = obj1['name']
            for pos2, obj2 in chunk2.iterrows():
                # print('reached')
                if obj1['Doctor Code'] != obj2['Doctor Code']:
                    name2 = obj2['name']
                    # print(name1)
                    name = self.name_matcher(name1, name2, 40)
                    # print('on 40', name)
                    # input('check')
                    if 16 < name < 32:
                        if obj1['mobile'] == obj2['mobile'] or obj2['email'] == obj1['email']:
                            score = self.field_checker(obj1=obj1, obj2=obj2, score=name, change=40)
                            if score >= 90:

                                # s = s + name1 + ' ' + name2 + ' ' + obj1['email'] + ' ' + obj2['email'] + ' ' + obj1['city']\
                                #     + ' ' + obj2['city'] + ' ' + str(obj1['mobile']) + ' ' + str(obj2['mobile']) + ' ' + \
                                #     obj1['speciality'] + ' ' + obj2['speciality'] + ' ' + obj1['gender'] + ' ' + \
                                #     obj2['gender'] + str(score) + ' '
                                # s = s + ' ' + str(pos2)
                                s.append(obj2['Doctor Code'])
                            # input('check')

                    elif name >= 32:
                        score = self.field_checker(obj1=obj1, obj2=obj2, score=name, change=40)
                        # print('>=32', name1, name2, score)
                        if score >= 90:
                            s.append(obj2['Doctor Code'])
                            # s = s + name1 + ' ' + name2 + ' ' + obj1['email'] + ' ' + obj2['email'] + ' ' + obj1['city'] \
                            #     + ' ' + obj2['city'] + ' ' + str(obj1['mobile']) + ' ' + str(obj2['mobile']) + ' ' + \
                            #     obj1['speciality'] + ' ' + obj2['speciality'] + ' ' + obj1['gender'] + ' ' + \
                            #     obj2['gender'] + str(score) + ' '
                            # s = s + str(pos2) + ' '
                            # result = (pos1, s)
            if s:
                p[obj1['Doctor Code']] = s
        # print('dup ', time.time() * 1000 - startTime)
        return p


