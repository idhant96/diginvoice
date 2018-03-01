from fuzzywuzzy import process
import multiprocessing
import pandas as pd
import sys
import re


class Big(object):
    @staticmethod
    def chunker(df, num_processes):
        chunk_size = int(df.shape[0] / num_processes)
        # print(chunk_size)
        chunks = [df.ix[df.index[i:i + chunk_size]] for i in range(0, df.shape[0], chunk_size)]
        objects = []
        for i in range(len(chunks)):
            for j in range(len(chunks)):
                if i <= j:
                    objects.append((chunks[i], chunks[j]))
        return objects

    @classmethod
    def process_dataframe(self, file_path):
        result = []
        df = pd.read_excel(file_path)
        df = df.fillna('')
        num_processes = multiprocessing.cpu_count() - 1
        pool = multiprocessing.Pool(processes=num_processes)
        male = df.loc[df['gender'] == 'Male']
        female = df.loc[df['gender'] == 'Female']
        male_chunks = self.chunker(male, num_processes)
        result.append(pool.starmap(self.dup, male_chunks))
        # print('male done')
        female_chunks = self.chunker(female, num_processes)
        result.append(pool.starmap(self.dup, female_chunks))
        # print('female done')
        # print(result)
        return result

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
    def absent_fields(obj1, obj2):
        ab = 0
        if obj1['email'] == obj2['email'] == '':
            ab= ab + 15
        if obj1['age'] == obj2['age'] == '':
            ab = ab + 5
        if obj1['city'] == obj2['city'] == '':
            ab = ab + 10
        if obj1['gender'] == obj2['gender'] == '':
            ab = ab + 5
        if obj1['speciality'] == obj2['speciality'] == '':
            ab = ab + 10
        if obj1['mobile'] == obj2['mobile'] == '':
            ab = ab + 15
        return ab

    @staticmethod
    def checker(field1, field2,  score, ad):
        # startTime = time.time() * 1000
        flag = 0
        if field1 == field2 == '':
            return score, flag+1
        if field1 == field2:
            score = score + ad
            # print('checker ', time.time() * 1000- startTime)
            return score, flag
        # print('checker ', time.time() * 1000 - startTime)
        return score, flag

    @classmethod
    def field_checker(self, obj1, obj2, score, change):
        heads = {'email':15, 'age':15, 'city':10, 'gender':5, 'speciality':5, 'mobile':15}
        ab = self.absent_fields(obj1, obj2)
        if ab > 0:
            ab = 100 - ab
            for head in heads.keys():
                heads[head] = 100 * (heads[head] / ab)
        name1 = obj1['name']
        name2 = obj2['name']
        name = score
        score = 0
        score, flag = self.checker(obj1['email'], obj2['email'], score=score, ad=heads['email'])
        # if flag > 0:
        #     change = change + 10
        #     name = self.name_matcher(name1, name2, change)
        score, flag = self.checker(obj1['age'], obj2['age'], score=score, ad=heads['age'])
        # if flag > 0:
        #     change = change + 10
        #     name = self.name_matcher(name1, name2, change)
        score, flag = self.checker(obj1['city'], obj2['city'], score=score, ad=heads['city'])
        # if flag > 0:
        #     change = change + 10
        #     name = self.name_matcher(name1, name2, change)
        score, flag = self.checker(obj1['gender'], obj2['gender'], score=score, ad=heads['gender'])
        # if flag > 0:
        #     change = change + 5
        #     name = self.name_matcher(name1, name2, change)
        score, flag = self.checker(obj1['speciality'], obj2['speciality'], score=score, ad=heads['speciality'])
        # if flag > 0:
        #     change = change + 10
        #     name = self.name_matcher(name1, name2, change)
        score, flag = self.checker(obj1['mobile'], obj2['mobile'], score=score, ad=heads['mobile'])
        # if flag > 0:
        #     change = change + 15
        #     name = self.name_matcher(name1, name2, change)
        # print('field_checkr ', time.time() * 1000 - startTime)
        return score, name

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
                if obj1['id'] != obj2['id'] and obj1['gender'] == obj2['gender'] and obj2['State'] == obj1['State']:
                    name2 = obj2['name']
                    # print(name1)
                    n1 = re.findall(r'DR(\s|\.)(.+)', obj1['name'].upper())
                    n2 = re.findall(r'DR(\s|\.)(.+)', obj2['name'].upper())
                    if n1:
                        name1 = n1[0][1]
                    if n2:
                        name2 = n2[0][1]
                    name = self.name_matcher(name1, name2, 35)
                    # print('on 40', name)
                    # input('check')
                    if 14 < name < 30.1:
                        if obj1['mobile'] == obj2['mobile'] or obj2['email'] == obj1['email']:
                            if obj1['mobile'] == '' or obj1['email'] == '':
                                continue
                            score, name = self.field_checker(obj1=obj1, obj2=obj2, score=name, change=35)
                            if score+name >= 80:
                                print(obj1['id'], obj2['id'], score, name)
                                # s = s + name1 + ' ' + name2 + ' ' + obj1['email'] + ' ' + obj2['email'] + ' ' + obj1['city']\
                                #     + ' ' + obj2['city'] + ' ' + str(obj1['mobile']) + ' ' + str(obj2['mobile']) + ' ' + \
                                #     obj1['speciality'] + ' ' + obj2['speciality'] + ' ' + obj1['gender'] + ' ' + \
                                #     obj2['gender'] + str(score) + ' '
                                # s = s + ' ' + str(pos2)
                                s.append(obj2['Doctor Code'])
                            # input('check')

                    elif name >= 30.2:
                        score, name = self.field_checker(obj1=obj1, obj2=obj2, score=name, change=35)
                        # print('>=32', name1, name2, score)
                        if score+name >= 80:
                            print(obj1['id'],obj2['id'], score, name)
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


