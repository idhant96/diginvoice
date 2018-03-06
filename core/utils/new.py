from fuzzywuzzy import process
import multiprocessing
import re
from copy import deepcopy
import sys


class Big(object):
    col_scores = {}

    col_names = {}
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
    def process_dataframe(cls, df, col_scores, col_names):
        cls.col_scores = col_scores
        cls.col_names = col_names
        result = []
        df = df.fillna('')
        num_processes = multiprocessing.cpu_count() - 1
        pool = multiprocessing.Pool(processes=num_processes)
        if 'gender' in col_names.keys():
            male = df.loc[df['gender'] == 'Male']
            female = df.loc[df['gender'] == 'Female']
            male_chunks = cls.chunker(male, num_processes)
            result.append(pool.starmap(cls.dup, male_chunks))
            print('male done')
            female_chunks = cls.chunker(female, num_processes)
            print(female.shape[0])
            result.append(pool.starmap(cls.dup, female_chunks))
            print('female done')
        else:
            chunks = cls.chunker(df, num_processes)
            result.append(pool.starmap(cls.dup, chunks))

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

    @classmethod
    def absent_fields(cls, obj1, obj2):
        ab = 0
        for col in cls.col_names.keys():
            if cls.col_names[col] is not None:
                if obj1[cls.col_names[col]] == obj2[cls.col_names[col]] == '':
                    ab = ab + cls.col_scores[col]
        return ab

    @staticmethod
    def checker(field1, field2, score, ad):
        if field1 == field2 == '':
            return score, 1
        if field1 == field2:
            score = score + ad
            # print('checker ', time.time() * 1000- startTime)
            return score, 0
        # print('checker ', time.time() * 1000 - startTime)
        return score, 0

    @classmethod
    def field_checker(cls, obj1, obj2, score):
        # heads = {'email':15, 'age':15, 'city':10, 'gender':5, 'speciality':5, 'mobile':15}
        ab = cls.absent_fields(obj1, obj2)
        scores = deepcopy(cls.col_scores)
        if ab > 0:
            print(ab)
            ab = 100 - ab
            for col in scores.keys():
                scores[col] = 100 * (scores[col] / ab)
        print(scores)
        name = score
        name_total = 35
        score = 0
        for field in cls.col_names.keys():
            if field in cls.col_scores.keys():
                score, flag= cls.checker(obj1[cls.col_names[field]], obj2[cls.col_names[field]], score=score, ad=scores[field])
                # if flag == 1:
                #     name_total = name_total + scores[field]
                #     name = cls.name_matcher(obj1[cls.col_names['name']], obj2[cls.col_names['name']], name_total)
                #     print(name)
        return score, name

    @classmethod
    def dup(cls, chunk1, chunk2):
        cols = cls.col_names
        p = {}
        for pos1, obj1 in chunk1.iterrows():
            s = []
            name1 = obj1[cols['name']]
            for pos2, obj2 in chunk2.iterrows():
                # print('reached')
                if obj1[cols['id']] != obj2[cols['id']]:
                    name2 = obj2[cols['name']]
                    # print(name1)
                    n1 = re.findall(r'DR(\s|\.)(.+)', obj1[cols['name']].upper())
                    n2 = re.findall(r'DR(\s|\.)(.+)', obj2[cols['name']].upper())
                    if n1:
                        name1 = n1[0][1]
                    if n2:
                        name2 = n2[0][1]
                    name = cls.name_matcher(name1, name2, 35)
                    # print('on 40', name)
                    # input('check')
                    if 14 < name < 30.1:
                        if cols['mobile'] and cols['email'] is not None:
                            if obj1[cols['mobile']] == obj2[cols['mobile']] or obj2[cols['email']] == obj1[cols['email']]:
                                if obj1[cols['mobile']] == '' or obj1[cols['email']] == '':
                                    continue
                                score, name = cls.field_checker(obj1, obj2, name)
                                if score+name >= 80:
                                    print(obj1['id'], obj2['id'], score, name)
                                    s.append(obj2['Doctor Code'])
                    elif name >= 30.2:
                        score, name = cls.field_checker(obj1, obj2, name)
                        # print('>=32', name1, name2, score)
                        if score+name >= 80:
                            print(obj1['id'],obj2['id'], score, name)
                            s.append(obj2['Doctor Code'])
            if s:
                p[obj1['Doctor Code']] = s
        # print('dup ', time.time() * 1000 - startTime)
        return p


