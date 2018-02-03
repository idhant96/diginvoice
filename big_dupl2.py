import pandas as pd
import re
from fuzzywuzzy import process


class Big(object):
    bigdata = pd.read_excel(
        'small.xlsx'
    )
    writer  = pd.ExcelWriter('result.xlsx')
    bigdata = bigdata.fillna('')
    bigdata['MatchSearchName'] = ''
    bigdata['match'] = ''
    print(bigdata.head(n=5))
    # input('head')
    for _, obj in bigdata.iterrows():
        obj.FIRST_NAME = re.sub(' +',' ',obj.DoctorName)

    for pos1, obj1 in bigdata.iterrows():
        p = ''
        name1 = obj1['DoctorName']
        bigdata.set_value(pos1, 'MatchSearchName', name1)
        for pos2, obj2 in bigdata.iterrows():
            if pos1 != pos2:

                name2 = obj2['DoctorName']
                n = []
                n.append(name2.upper())
                # partial = fuzz.partial_ratio(name1.upper(), name2.upper())
                token1 = process.extract(name1.upper(), n, limit=3)

                # print(name1, name2)
                token = token1[0][1]

                # print(pos1+2, pos2+2)
                if token > 80:
                    part = 0
                    score = (token/100)*40

                    # input('check')
                    if score < 33:
                        continue
                    print(name1, name2, score)
                    age1 = obj1['Age']
                    age2 = obj2['Age']

                    if age1 == age2 or age1==age2=='':
                        score = score + 15

                    gender1 = obj1['Sex']
                    gender2 = obj2['Sex']

                    if gender1 == gender2 or gender2==gender1=='':
                        score = score + 15

                    zone1 = obj1['CityName']
                    zone2 = obj2['CityName']

                    if zone1 == zone2 or zone2==zone1=='':
                        score = score + 15

                    spec1 = obj1['Specialization']
                    spec2 = obj2['Specialization']
                    if spec1 == spec2:
                        score = score + 15
                    # print(score)
                    # input('check2')
                    if score >= 90:

                        # print(name1, name2, score, pos1, pos2)
                        s = name1 + ',' + name2 + ' '+spec1+' '+spec2+' ' + gender2 + ' ' + gender2 + ' ' + str(age1) + ' ' + str(age2) + ' ' + zone1 + ' ' + zone2 + '\n'
                        p = p + name2 + '-' + str(pos2 + 2) + '  '

                        bigdata.set_value(pos1, 'match', p)
                        print(s)
                        # fl.write(s)
                        # input('lol')

    bigdata.to_excel(writer, 'sheet1')
    writer.save()
    # fl.close()