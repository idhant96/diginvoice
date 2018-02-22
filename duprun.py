from core.utils.new import Big
import pandas as pd
import time
import sys


path = sys.argv[1]
odf = pd.read_excel(path)
startTime = time.time() * 1000
result = Big.get_pos(path)
# df['MatchSearchName'] = ''
# df['match'] = ''
# print(result)
# cols = ['pos','name', 'email', 'mobile', 'gender', 'age', 'city', 'speciality']

df = pd.DataFrame(columns=list(odf.columns.values))
# df = pd.DataFrame()
writer = pd.ExcelWriter('newcode.xlsx')

for p in result:
    for pos1 in p.keys():
        df = df.append(odf.loc[odf['Doctor Code'] == pos1])
        for pos2 in p[pos1]:
            df = df.append(odf.loc[odf['Doctor Code'] == pos2])
        # df.at[pos1, 'MatchSearchName'] = df.iloc[pos1, 2]
        # df.at[pos1, 'match'] = p[pos1]

df.to_excel(writer, 'sheet1')
writer.save()
print('complete ', time.time() * 1000 - startTime)
