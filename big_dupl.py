import pandas as pd
import re
import distance
import sys
from fuzzywuzzy import fuzz

class Big(object):
    bigdata = pd.read_csv(
        'csvs/snall_docs.csv'
    )
    fl = open('result.txt', 'w')
    bigdata = bigdata.fillna('')
    specs_names = {}
    for _, obj in bigdata.iterrows():
        obj.FIRST_NAME = re.sub(' +',' ',obj.DoctorName)

    for _, obj in bigdata.iterrows():
        # print(obj.Specialization)
        if obj.Specialization not in specs_names:
            specs_names[obj.Specialization] = []
        else:
            specs_names[obj.Specialization].append(int(obj['Doctor Code']))
    # print(specs_names)
    # sys.exit())
    for spec in specs_names.keys():
        if spec == 'Paediatrician':
            break
        names = []
        # input('first lol')
        for val1 in specs_names[spec]:
            for val2 in specs_names[spec]:
                if val1 != val2:
                    name1 = bigdata.loc[bigdata['Doctor Code'] == val1, 'DoctorName'].iloc[0]
                    name2 = bigdata.loc[bigdata['Doctor Code'] == val2, 'DoctorName'].iloc[0]
                    n1 = name1.split(' ')
                    n2 = name2.split(' ')
                    jac_sum = 0
                    # if len(n1) <= len(n2):
                    #     for words1 in n1:
                    #         for words2 in n2:
                    #             d = 1 - distance.jaccard(words1.upper(), words2.upper())
                    #             jac_sum = jac_sum + d
                    # elif len(n1) > len(n2):
                    #     for words1 in n2:
                    #         for words2 in n1:
                    #             d = 1 - distance.jaccard(words1.upper(), words2.upper())
                    #             jac_sum = jac_sum + d
                    # lent = len(n1)*len(n2)
                    # print(name1, name2, lent, (jac_sum/lent)*100)
                    # if (jac_sum/lent)*100 > 36:
                    #     input('check')
                    # continue
                    words1 = name1.replace('.', ' ').split(' ')
                    words2 = name2.replace('.', ' ').split(' ')
                    jac = 1 - distance.jaccard(name1.upper(), name2.upper())
                    f = fuzz.partial_ratio(name1.upper(), name2.upper())
                    pos1 = bigdata.loc[bigdata['Doctor Code'] == val1].index[0]
                    pos2 = bigdata.loc[bigdata['Doctor Code'] == val2].index[0]
                    age1 = bigdata['Age'].iloc[pos1]
                    age2 = bigdata['Age'].iloc[pos2]
                    print(name1, name2, age1, age2)
                    if age1 == age2 and f > 70:
                        # input('entered')
                        # print(name1, name2)
                        score = 70
                        # print(name1, pos1, name2, pos2, jac)
                        # sys.exit()
                        gender1 = bigdata['Sex'].iloc[pos1]
                        gender2 = bigdata['Sex'].iloc[pos2]
                        print(gender1, gender2)
                        if gender1 == gender2:
                            score = score + 15

                        print(age1, age2)

                        zone1 = bigdata['CityName'].iloc[pos1]
                        zone2 = bigdata['CityName'].iloc[pos2]
                        print(zone1, zone2)
                        if zone1 == zone2:
                            score = score + 15
                        # print(score)
                        # input('scheck score')
                        if score > 85:
                            # print(name1, name2, score, pos1, pos2)
                            s = name1 + ' ' + name2 + ' ' + str(f) + '\n'
                            print(s)
                            fl.write(s)
                            # input('lol')
    fl.close()