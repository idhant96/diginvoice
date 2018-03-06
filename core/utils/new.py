from fuzzywuzzy import process
import multiprocessing
import re


class Big(object):
    columns = {}
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
    def process_dataframe(cls, df, cols):
        cls.columns = cols
        result = []
        df = df.fillna('')
        num_processes = multiprocessing.cpu_count() - 1
        pool = multiprocessing.Pool(processes=num_processes)
        if 'gender' in cols.keys():
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
            chunks = self.chunker(df, num_processes)
            result.append(pool.starmap(self.dup, chunks))
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
        if field1 == field2 == '':
            return score
        if field1 == field2:
            score = score + ad
            # print('checker ', time.time() * 1000- startTime)
            return score
        # print('checker ', time.time() * 1000 - startTime)
        return score

    @classmethod
    def field_checker(self, obj1, obj2, score, change):
        heads = {'email':15, 'age':15, 'city':10, 'gender':5, 'speciality':5, 'mobile':15}
        ab = self.absent_fields(obj1, obj2)
        if ab > 0:
            ab = 100 - ab
            for head in heads.keys():
                heads[head] = 100 * (heads[head] / ab)
        name = score
        score = 0
        score= self.checker(obj1['email'], obj2['email'], score=score, ad=heads['email'])
        score= self.checker(obj1['age'], obj2['age'], score=score, ad=heads['age'])
        score = self.checker(obj1['city'], obj2['city'], score=score, ad=heads['city'])
        score = self.checker(obj1['gender'], obj2['gender'], score=score, ad=heads['gender'])
        score = self.checker(obj1['speciality'], obj2['speciality'], score=score, ad=heads['speciality'])
        score = self.checker(obj1['mobile'], obj2['mobile'], score=score, ad=heads['mobile'])
        return score, name

    @classmethod
    def dup(cls, chunk1, chunk2):
        # name = str(cls.columns['name'])
        # id = str(cls.columns['id'])
        # age = str(cls.columns['age'])
        # email = str(cls.columns['email'])

        p = {}
        for pos1, obj1 in chunk1.iterrows():
            s = []
            name1 = obj1[]
            for pos2, obj2 in chunk2.iterrows():
                # print('reached')
                if obj1['id'] != obj2['id'] and obj2['State'] == obj1['State']:
                    name2 = obj2['name']
                    # print(name1)
                    n1 = re.findall(r'DR(\s|\.)(.+)', obj1['name'].upper())
                    n2 = re.findall(r'DR(\s|\.)(.+)', obj2['name'].upper())
                    if n1:
                        name1 = n1[0][1]
                    if n2:
                        name2 = n2[0][1]
                    name = cls.name_matcher(name1, name2, 35)
                    # print('on 40', name)
                    # input('check')
                    if 14 < name < 30.1:
                        if obj1['mobile'] == obj2['mobile'] or obj2['email'] == obj1['email']:
                            if obj1['mobile'] == '' or obj1['email'] == '':
                                continue
                            score, name = cls.field_checker(obj1=obj1, obj2=obj2, score=name, change=35)
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
                        score, name = cls.field_checker(obj1=obj1, obj2=obj2, score=name, change=35)
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


