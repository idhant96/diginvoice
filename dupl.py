import pandas as pd


class Dupl(object):
    match_names = []
    df = pd.read_csv('doct.csv')
    df = df.fillna('')
    specs_names = {}
    x = df['FIRST_NAME']
    # print(x[x=='HEMATOLOGIST'])
    df['FIRST_NAME'] = df['FIRST_NAME'] + ' ' + df['MIDDLE_NAME'] + ' ' + df['LAST_NAME']
    score = 0

    for pos, obj in df.iterrows():
        if obj.Speciality_Name not in specs_names:
            specs_names[obj.Speciality_Name] = []
        else:
            specs_names[obj.Speciality_Name].append(pos)
    print(specs_names.keys())

    for spec in specs_names.keys():
        names = []
        for positions in specs_names[spec]:
            # print(positions)
            names.append(df.iloc[positions].FIRST_NAME)
        print(spec)
        # print(names)
        input(''.format(spec))
        for name1 in names:
            for name2 in names:
                if names.index(name1) != names.index(name2):
                    q = name1.replace('.', ' ')
                    w = name2.replace('.', ' ')
                    words1 = q.split(' ')
                    words2 = w.split(' ')
                    flag = 0
                    l = 0
                    if len(words1) > len(words2):
                        l = len(words2)
                        for word in words2:
                            if word in words1:
                                flag = flag + 1
                    else:
                        l = len(words1)
                        for word in words1:
                            if word in words2:
                                flag = flag + 1
                    if flag == l:
                        # print(name1, name2)
                        score = 28
                        pos2 = x[x == name2].index[0]
                        pos1 = x[x == name1].index[0]
                        # hs = df['HOSPITAL_ATTACHED1']
                        role1 = df['Role'].iloc[pos1]
                        role2 = df['Role'].iloc[pos2]
                        if role1 == role2:
                            score = score + 14
                        pract1 = df['Practise'].iloc[pos1]
                        pract2 = df['Practise'].iloc[pos2]
                        if pract1 == pract2:
                            score = score + 14
                        zone1 = df['ZONE'].iloc[pos1]
                        zone2 = df['ZONE'].iloc[pos2]
                        if zone1 == zone2:
                            score = score + 14
                        ter1 = df['TERRITORY'].iloc[pos1]
                        ter2 = df['TERRITORY'].iloc[pos2]
                        if ter1 == ter2:
                            score = score + 14
                        # if score > 80:
                        print(name1, name2, score, pos1, pos2)




