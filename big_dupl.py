import pandas as pd
import re
import distance


class Big(object):
    bigdata = pd.read_csv(
        'csvs/small_docs.csv'
    )
    bigdata = bigdata.fillna('')
    specs_names = {}
    for _, obj in bigdata.iterrows():
        obj.FIRST_NAME = re.sub(' +',' ',obj.DoctorName)

    for pos, obj in bigdata.iterrows():
        # print(obj.Specialization)
        if obj.Specialization not in specs_names:
            specs_names[obj.Specialization] = []
        else:
            specs_names[obj.Specialization].append(pos)
    # print(specs_names.keys())
    specs = {}
    for spec in specs_names.keys():
        specs[spec] = specs_names[spec]
        if spec == 'physician1':
            break
    # print(specs)
    # sys.exit()
    for spec in specs.keys():
        names = []
        for positions in specs[spec]:
            # print(positions)
            names.append(bigdata.iloc[positions].DoctorName)
        print(spec)
        print(names)
        # sys.exit()
        input('first lol')
        for name1 in names:
            for name2 in names:
                # print(name1, name2)
                if names.index(name1) != names.index(name2):
                    q = name1.replace('.', ' ')
                    w = name2.replace('.', ' ')
                    words1 = q.split(' ')
                    words2 = w.split(' ')
                    print(name1, name2)
                    jac = 1 - distance.jaccard(name1.upper(), name2.upper())
                    if jac > 0.75:
                        input('entered')
                        # print(name1, name2)
                        score = 55
                        pos1 = bigdata['DoctorName'][bigdata['DoctorName'] == name1].index[0]
                        pos2 = bigdata['DoctorName'][bigdata['DoctorName'] == name2].index[0]
                        print(name1, pos1, name2, pos2)
                        # sys.exit()
                        gender1 = bigdata['Sex'].iloc[pos1]
                        gender2 = bigdata['Sex'].iloc[pos2]
                        print(gender1, gender2)
                        if gender1 == gender2:
                            score = score + 15
                        age1 = bigdata['Age'].iloc[pos1]
                        age2 = bigdata['Age'].iloc[pos2]
                        print(age1, age2)
                        if age1 == age2:
                            score = score + 15
                        zone1 = bigdata['CityName'].iloc[pos1]
                        zone2 = bigdata['CityName'].iloc[pos2]
                        print(zone1, zone2)
                        if zone1 == zone2:
                            score = score + 15
                        print(score)
                        input('scheck score')
                        if score > 80:
                            print(name1, name2, score, pos1, pos2)
                            input('lol')